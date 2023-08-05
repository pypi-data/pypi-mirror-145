import sys
from dataclasses import dataclass
from typing import List, Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse
from slck.utils import confirm_user_input


class ChannelNotFoundError(Exception):
    pass


@dataclass
class Channel:
    id: str
    name: str


class ChannelManager:
    def __init__(self, client: WebClient) -> None:
        self.client: WebClient = client

    def list(self, prefix: str = "") -> List[Channel]:
        next_cursor: str = ""  # for pagenation
        hit_channels: List[Channel] = []
        while True:
            response: SlackResponse = self.client.conversations_list(
                types="public_channel,private_channel",
                limit=200,
                cursor=next_cursor,
            )
            for channel in response["channels"]:
                channel_name = channel["name_normalized"]
                if channel_name.startswith(prefix):
                    hit_channels.append(Channel(channel["id"], channel_name))
            next_cursor = response["response_metadata"]["next_cursor"]
            if not next_cursor:
                break
        return hit_channels

    def find(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
    ) -> List[Channel]:
        prefix = "" if name is None else name
        channels: List[Channel] = []
        for channel in self.list(prefix=prefix):
            if id is None or channel.id == id:
                if name is None or channel.name == name:
                    channels.append(channel)
        if not channels:
            raise ChannelNotFoundError
        assert len(channels) == 1
        return channels

    def archive(self, prefix: str, yes: bool = False) -> List[Channel]:
        target_channels: List[Channel] = self.list(prefix=prefix)
        if not target_channels:
            raise ChannelNotFoundError(f"No channels found (prefix={prefix})")
        for channel in target_channels:
            sys.stdout.write(f"{channel}\n")
        archived_channels: List[Channel] = []
        if yes or confirm_user_input(
            f"Do you want to archive {len(target_channels):,d} channels?"
        ):
            for channel in target_channels:
                self.client.conversations_join(channel=channel.id)
                response_for_archive: SlackResponse = self.client.conversations_archive(
                    channel=channel.id
                )
                if response_for_archive["ok"]:
                    sys.stdout.write(f"Archived channel: {channel}" + "\n")
                    archived_channels.append(channel)
        else:
            sys.stdout.write(
                f"Don't worry! {len(target_channels):,d} channels were left unchanged."
                + "\n"
            )
        return archived_channels
