from datetime import datetime
from typing import Any
from typing import Mapping

from app.common import logging
from app.common import settings
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.beatmaps import BeatmapsRepo
from app.services.osu_api import OsuAPIRequestError


async def create(ctx: Context, beatmap_id: int, md5_hash: str, set_id: int,
                 convert: bool, mode: str, od: float, ar: float, cs: float,
                 hp: float, bpm: float, hit_length: int, total_length: int,
                 count_circles: int, count_sliders: int, count_spinners: int,
                 difficulty_rating: float, is_scoreable: bool, pass_count: int,
                 play_count: int, version: str, created_by: int,
                 ranked_status: int, status: str,
                 ) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsRepo(ctx)

    beatmap = await repo.create(beatmap_id=beatmap_id, md5_hash=md5_hash,
                                set_id=set_id, convert=convert, mode=mode,
                                od=od, ar=ar, cs=cs, hp=hp, bpm=bpm,
                                hit_length=hit_length, total_length=total_length,
                                count_circles=count_circles,
                                count_sliders=count_sliders,
                                count_spinners=count_spinners,
                                difficulty_rating=difficulty_rating,
                                is_scoreable=is_scoreable, pass_count=pass_count,
                                play_count=play_count, version=version,
                                created_by=created_by,
                                ranked_status=ranked_status, status=status)
    if beatmap is None:
        return ServiceError.BEATMAPS_CANNOT_CREATE

    return beatmap


def is_expired(beatmap: Mapping[str, Any]) -> bool:
    last_update: datetime = beatmap["updated_at"]

    return (datetime.now() - last_update).total_seconds() >= 60 * 60 * 24


async def fetch_one(ctx: Context, beatmap_id: int
                    ) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsRepo(ctx)

    beatmap = await repo.fetch_one(beatmap_id=beatmap_id)
    if beatmap is None:
        expired = False
    else:
        expired = is_expired(beatmap)
        if expired:
            await repo.delete(beatmap_id)

    if beatmap is None or expired:
        # try to get it from the osu! api
        try:
            osu_beatmap = await ctx.osu_api_client.get_beatmap(beatmap_id)
        except OsuAPIRequestError as exc:
            logging.error("Failed to fetch beatmap from osu! api: ",
                          response_code=exc.status_code, message=exc.message)
            return ServiceError.BEATMAPS_NOT_FOUND

        beatmap = await repo.create(beatmap_id=osu_beatmap["id"],
                                    md5_hash=osu_beatmap["checksum"],
                                    set_id=osu_beatmap["beatmapset_id"],
                                    convert=osu_beatmap["convert"],
                                    mode=osu_beatmap["mode"],
                                    od=osu_beatmap["accuracy"],
                                    ar=osu_beatmap["ar"],
                                    cs=osu_beatmap["cs"],
                                    hp=osu_beatmap["drain"],
                                    bpm=osu_beatmap["bpm"],
                                    hit_length=osu_beatmap["hit_length"],
                                    total_length=osu_beatmap["total_length"],
                                    count_circles=osu_beatmap["count_circles"],
                                    count_sliders=osu_beatmap["count_sliders"],
                                    count_spinners=osu_beatmap["count_spinners"],
                                    difficulty_rating=osu_beatmap["difficulty_rating"],
                                    is_scoreable=osu_beatmap["is_scoreable"],
                                    pass_count=osu_beatmap["passcount"],
                                    play_count=osu_beatmap["playcount"],
                                    version=osu_beatmap["version"],
                                    created_by=osu_beatmap["user_id"],
                                    ranked_status=osu_beatmap["ranked"],
                                    status=Status.ACTIVE)
        if beatmap is None:
            # return ServiceError.BEATMAPS_CANNOT_CREATE
            return ServiceError.BEATMAPS_NOT_FOUND

    return beatmap


async def fetch_many(ctx: Context, set_id: int | None = None,
                     md5_hash: str | None = None,
                     mode: str | None = None,
                     ranked_status: int | None = None,
                     status: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ) -> list[Mapping[str, Any]]:
    repo = BeatmapsRepo(ctx)

    beatmaps = await repo.fetch_many(set_id=set_id,
                                     md5_hash=md5_hash,
                                     mode=mode,
                                     ranked_status=ranked_status,
                                     status=status,
                                     page=page,
                                     page_size=page_size)

    return beatmaps


async def delete(ctx: Context, beatmap_id: int
                 ) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsRepo(ctx)

    beatmap = await repo.delete(beatmap_id=beatmap_id)
    if beatmap is None:
        return ServiceError.BEATMAPS_NOT_FOUND

    return beatmap
