from enum import Enum
from .SquadsClient import client
from typing import Optional


class SquadRole(Enum):
    member = 0
    moder = 1
    admin = 2
    owner = 3


class UserSquad:
    def __init__(self, data: dict):
        self._data = data
        self.user_id: int = data["user_id"]
        self.squad_id: int = data["squad_id"]
        self.squad_role: SquadRole = SquadRole(data["squad_role"])

    def __repr__(self):
        return str(self._data)

    async def leave_squad(self, requester_id: int) -> Optional[tuple['UserSquad', ...]]:
        """Покинуть сквад"""
        response = client.delete(f"/squads/{self.squad_id}/members/{self.user_id}", {"called_user_id": requester_id})
        if response.get("error"):
            return None
        return tuple(map(UserSquad, response))


def get_user_squad(user_id: int) -> Optional[UserSquad]:
    """Получить сквад пользователя по его айди"""
    response = client.get(f"/users/{user_id}")
    if response.get("error"):
        return None
    return UserSquad(response)
