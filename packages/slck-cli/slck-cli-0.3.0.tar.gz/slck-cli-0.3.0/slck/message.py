from dataclasses import dataclass
from typing import Dict, List

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse
from slck.channel import Channel, ChannelManager
from slck.user import User, UserManager
from slck.utils import confirm_user_input


@dataclass
class Message:
    message_type: str
    user: User
    channel: Channel
    ts: str
    text: str
    num_reply: int
    num_replyuser: int
    num_reaction: int
    permalink: str = ""

    def identify_user(self, client: WebClient) -> None:
        um: UserManager = UserManager(client)
        self.user = um.find(id=self.user.id)[0]

    def get_permalink(self, client: WebClient) -> None:
        self.permalink: str = client.chat_getPermalink(
            channel=self.channel.id, message_ts=self.ts
        )["permalink"]


def parse_message(message: Dict, channel: Channel) -> Message:
    message_type: str = message["type"]
    user: User = User(id=message["user"])
    ts: str = message["ts"]
    text: str = message["text"]
    num_reply: int = message.get("reply_count", 0)
    num_replyuser: int = len(message.get("reply_users", []))
    reactions: List = message.get("reactions", [])
    num_reaction = sum([reaction.get("count", 0) for reaction in reactions])
    return Message(
        message_type=message_type,
        user=user,
        channel=channel,
        ts=ts,
        text=text,
        num_reply=num_reply,
        num_replyuser=num_replyuser,
        num_reaction=num_reaction,
    )


class MessageManager:
    def __init__(self, client: WebClient) -> None:
        self.client = client

    def list(
        self,
        channel: str,  # channel id or channel name (depends on argument `name`)
        name: bool = True,  # if False, `channel` is considered as channel ID
    ) -> List[Message]:
        cm: ChannelManager = ChannelManager(self.client)
        c: Channel = cm.find(name=channel)[0] if name else cm.find(id=channel)[0]
        messages: List[Message] = []
        next_cursor: str = ""  # for pagenation
        while True:
            response: SlackResponse = self.client.conversations_history(
                channel=c.id, next_cursor=next_cursor
            )
            for message in response["messages"]:
                if message["type"] == "message":
                    m = parse_message(message, channel=c)
                    m.identify_user(self.client)
                    messages.append(m)
            if response["has_more"] is True:
                next_cursor = response["response_metadata"]["next_cursor"]
            else:
                break
        return messages

    def popular(
        self,
        channel: str,  # channel id or channel name (depends on argument `name`)
        name: bool = True,  # if False, `channel` is considered as channel ID
        k: int = 1,
        permalink: bool = True,
    ) -> List[Message]:
        messages: List[Message] = sorted(
            self.list(channel, name), key=lambda m: m.num_reaction, reverse=True
        )
        messages = messages[: min(len(messages), k)]

        if permalink:
            for m in messages:
                m.get_permalink(self.client)

        return messages[: min(len(messages), k)]

    def award(self, channel: str, post: bool = False) -> str:
        popular_message: Message = self.popular(
            channel=channel, name=True, k=1, permalink=True
        )[0]
        userid: str = popular_message.user.id
        username = popular_message.user.name
        posting_text: str = (
            f"最もリアクションを獲得したのは <@{userid}|{username}>さんのこのポスト！"
            f"おめでとうございます！:raised_hands:\n{popular_message.permalink}"
        )
        if post:
            if confirm_user_input(
                f"""
Bot is about to post award message:
  {posting_text}
to {channel}. Are you sure?"""
            ):
                self.client.chat_postMessage(channel=channel, text=posting_text)
                return "Posted!"
            else:
                return "Award was canceled from user input."
        return posting_text
