import fire
from slack_sdk import WebClient
from slck.channel import ChannelManager
from slck.message import MessageManager
from slck.user import UserManager
from slck.utils import get_token


class SlackManager:
    def __init__(self, client: WebClient) -> None:
        self.__client = client
        self.channel = ChannelManager(self.__client)
        self.user = UserManager(self.__client)
        self.message = MessageManager(self.__client)


def main() -> None:
    token: str = get_token()
    client: WebClient = WebClient(token)
    slack: SlackManager = SlackManager(client)
    fire.Fire(slack)
