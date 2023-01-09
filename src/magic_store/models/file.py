from uuid import uuid4
from typing import Union


class File:
    def __init__(self, filename: str, path: str, id: Union[None, str] = None):
        self.id = id or str(uuid4())
        self.filename = filename
        self.path = path

    def __repr__(self) -> str:
        return str(self.__dict__)

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
