from app.common.context import Context
from app.services import database
from app.services import osu_api
from app.services import redis
from fastapi import Request


class RequestContext(Context):
    def __init__(self, request: Request) -> None:
        self.request = request

    @property
    def db(self) -> database.ServiceDatabase:
        return self.request.state.db

    @property
    def redis(self) -> redis.ServiceRedis:
        return self.request.state.redis

    @property
    def osu_api_client(self) -> osu_api.OsuAPIClient:
        return self.request.state.osu_api_client
