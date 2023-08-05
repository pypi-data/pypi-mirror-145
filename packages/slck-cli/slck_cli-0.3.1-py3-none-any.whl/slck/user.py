from dataclasses import dataclass
from typing import List, Optional

from slack_sdk import WebClient
from slack_sdk.web import SlackResponse


@dataclass
class User:
    id: str
    name: Optional[str] = None
    real_name: Optional[str] = None


class UserNotFoundError(Exception):
    pass


class UserManager:
    def __init__(self, client: WebClient) -> None:
        self.client = client

    def list(self) -> List[User]:
        next_cursor: str = ""  # for pagenation
        hit_users: List[User] = []
        while True:
            response: SlackResponse = self.client.users_list(
                limit=200, cursor=next_cursor
            )
            for user in response["members"]:
                if user["is_bot"]:
                    pass
                hit_users.append(
                    User(
                        id=user["id"],
                        name=user["name"],
                        real_name=user.get("real_name", None),
                    )
                )
            next_cursor = response["response_metadata"]["next_cursor"]
            if not next_cursor:
                break
        return hit_users

    def find(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        real_name: Optional[str] = None,
    ) -> List[User]:
        users: List[User] = []
        for user in self.list():
            if id is None or user.id == id:
                if name is None or user.name == name:
                    if real_name is None or user.real_name == real_name:
                        users.append(user)
        if not users:
            raise UserNotFoundError
        assert len(users) == 1
        return users
