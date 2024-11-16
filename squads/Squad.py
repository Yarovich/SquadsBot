from datetime import datetime
from .SquadsClient import client
from .UserSquad import UserSquad
from typing import Optional


class Squad:
    def __init__(self, data: dict):
        self._data = data
        self.squad_id: str = data["squad_id"]
        self.name: str = data["name"]
        self.short_name: str = data["short_name"]
        self.description: str = data["description"]
        self.public: bool = data["public"]
        self.create_date: datetime.strptime(data["create_date"], "%Y-%m-%d %H:%M:%S")
        self.max_members: int = data["max_members"]
        self.role_color: str = data["role_color"]
        self.embed_color: str = data["embed_color"]
        self.premium: bool = True if self.max_members == 0 else False

    def __repr__(self):
        return str(self._data)

    def get_members(self) -> Optional[tuple[UserSquad, ...]]:
        """Получить список участников сквада"""
        response = client.get(f"/squads/{self.squad_id}/members")
        if not isinstance(response, list):
            return None
        return tuple(map(UserSquad, response))

    async def add_member(self, user_id: int, requester_user_id: int) -> Optional[UserSquad]:
        """Добавить пользователя в сквад"""
        response = client.post(f"/squads/{self.squad_id}/members",
            {
                "user_id": user_id,
                "called_user_id": requester_user_id
            }
        )
        if response.get("error"):
            return None
        return UserSquad(response)

    async def edit(self,
             requester_user_id: int,
             name: Optional[str] = None,
             short_name: Optional[str] = None,
             description: Optional[str] = None,
             public: Optional[bool] = None,
             role_color: Optional[str] = None,
             embed_color: Optional[str] = None
        ) -> Optional['Squad']:
        """Изменить сквад"""
        response = client.put(f"/squads/{self.squad_id}",
            {
                "name": name or self.name,
                "short_name": short_name or self.short_name,
                "description": description or self.description,
                "public": public or self.public,
                "embed_color": embed_color or self.embed_color,
                "role_color": role_color or self.role_color,
                "user_id": requester_user_id
            }
        )
        if response.get("error"):
            return None
        return Squad(response)

    async def delete(self, requester_user_id: int) -> Optional['Squad']:
        """Удалить сквад"""
        response = client.delete(f"/squads/{self.squad_id}", {"user_id": requester_user_id})
        if response.get("error"):
            return None
        return Squad(response)


async def create_squad(name: str, short_name: str, owner_id: int) -> Optional[Squad]:
    """Создать новый сквад"""
    response = client.post("/squads", {"name": name, "short_name": short_name, "owner_id": owner_id})
    if response.get("error"):
        return None
    return Squad(response)


def get_squad(squad_id: int) -> Optional[Squad]:
    """Получить сквад по его айди"""
    response = client.get(f"/squads/{squad_id}")
    if response.get("error"):
        return None
    return Squad(response)


def get_all_squads() -> Optional[tuple[Squad, ...]]:
    """Получить список всех существующих сквадов"""
    response = client.get("/squads")
    if response.get("error"):
        return None
    return tuple(map(Squad, response))
