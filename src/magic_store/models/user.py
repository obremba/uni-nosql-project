from uuid import uuid4
from typing import Union


class User:
    def __init__(self, name: str, username: str, email: str, id: Union[None, str] = None):
        self.id = id or str(uuid4())
        self.name = name
        self.username = username
        self.email = email

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return self.__repr__()
