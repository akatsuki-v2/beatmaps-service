from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.services import database
from app.services import osu_api
from app.services import redis


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...

    @property
    @abstractmethod
    def redis(self) -> redis.ServiceRedis:
        ...

    @property
    @abstractmethod
    def osu_api_client(self) -> osu_api.OsuAPIClient:
        ...
