from typing import Any
from typing import Mapping

from app.common import settings
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.beatmaps import BeatmapsRepo
from app.repositories.beatmaps import RankedStatus


async def create(ctx: Context, beatmap_id: int, md5_hash: str, set_id: int,
                 convert: bool, mode: int, od: float, ar: float, cs: float,
                 hp: float, bpm: float, hit_length: int, total_length: int,
                 count_circles: int, count_sliders: int, count_spinners: int,
                 difficulty_rating: float, is_scorable: bool, pass_count: int,
                 play_count: int, version: str, created_by: str,
                 ranked_status: RankedStatus, status: Status, created_at: str,
                 updated_at: str, deleted_at: str
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
                                is_scorable=is_scorable, pass_count=pass_count,
                                play_count=play_count, version=version,
                                created_by=created_by,
                                ranked_status=ranked_status, status=status,
                                created_at=created_at, updated_at=updated_at,
                                deleted_at=deleted_at)
    if beatmap is None:
        return ServiceError.BEATMAPS_CANNOT_CREATE

    return beatmap


async def fetch_one(ctx: Context, beatmap_id: int) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsRepo(ctx)

    beatmap = await repo.fetch_one(beatmap_id=beatmap_id)
    if beatmap is None:
        return ServiceError.BEATMAPS_NOT_FOUND

    return beatmap


async def fetch_many(ctx: Context, set_id: int | None = None,
                     mode: int | None = None,
                     ranked_status: RankedStatus | None = None,
                     status: Status | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ) -> list[Mapping[str, Any]]:
    repo = BeatmapsRepo(ctx)

    beatmaps = await repo.fetch_many(set_id=set_id,
                                     mode=mode,
                                     ranked_status=ranked_status,
                                     status=status,
                                     page=page,
                                     page_size=page_size)

    return beatmaps


async def delete(ctx: Context, beatmap_id: int) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsRepo(ctx)

    beatmap = await repo.delete(beatmap_id=beatmap_id)
    if beatmap is None:
        return ServiceError.BEATMAPS_NOT_FOUND

    return beatmap
