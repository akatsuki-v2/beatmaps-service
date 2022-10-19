from datetime import datetime
from typing import Any
from typing import Mapping

from app.common import logging
from app.common import settings
from app.common.context import Context
from app.common.errors import ServiceError
from app.models import Status
from app.repositories.beatmaps import BeatmapsRepo
from app.repositories.beatmapsets import BeatmapsetsRepo
from app.services.osu_api import OsuAPIRequestError


async def create(ctx: Context, beatmapset_id: int, artist: str, artist_unicode: str,
                 covers: dict[str, Any], creator: str, favourite_count: int,
                 nsfw: bool, osu_play_count: int, preview_url: str,
                 source: str, title: str, title_unicode: str,
                 created_by: int, video: bool, download_disabled: bool,
                 availability_information: str | None, bpm: float,
                 can_be_hyped: bool, discussion_locked: bool,
                 current_hype: int, required_hype: int, is_scoreable: bool,
                 legacy_thread_url: str, current_nominations: int,
                 required_nominations: int, ranked_status: int, storyboard: bool,
                 osu_submitted_at: datetime, osu_updated_at: datetime,
                 osu_ranked_at: datetime, tags: str,
                 ) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsetsRepo(ctx)

    beatmapset = await repo.create(beatmapset_id=beatmapset_id, artist=artist,
                                   artist_unicode=artist_unicode,
                                   covers=covers, creator=creator,
                                   favourite_count=favourite_count, nsfw=nsfw,
                                   osu_play_count=osu_play_count,
                                   preview_url=preview_url, source=source,
                                   title=title, title_unicode=title_unicode,
                                   created_by=created_by, video=video,
                                   download_disabled=download_disabled,
                                   availability_information=availability_information,
                                   bpm=bpm, can_be_hyped=can_be_hyped,
                                   discussion_locked=discussion_locked,
                                   current_hype=current_hype,
                                   required_hype=required_hype,
                                   is_scoreable=is_scoreable,
                                   legacy_thread_url=legacy_thread_url,
                                   current_nominations=current_nominations,
                                   required_nominations=required_nominations,
                                   ranked_status=ranked_status,
                                   storyboard=storyboard, tags=tags,
                                   osu_submitted_at=osu_submitted_at,
                                   osu_updated_at=osu_updated_at,
                                   osu_ranked_at=osu_ranked_at,
                                   status=Status.ACTIVE)

    if beatmapset is None:
        return ServiceError.BEATMAPSETS_CANNOT_CREATE

    return beatmapset


def is_expired(beatmapset: Mapping[str, Any]) -> bool:
    last_update: datetime = beatmapset["updated_at"]

    return (datetime.now() - last_update).total_seconds() >= 60 * 60 * 24


async def fetch_one(ctx: Context, beatmapset_id: int) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsetsRepo(ctx)

    beatmapset = await repo.fetch_one(beatmapset_id)
    if beatmapset is None:
        expired = False
    else:
        expired = is_expired(beatmapset)
        if expired:
            await repo.delete(beatmapset_id)

    if beatmapset is None or expired:
        # fetch from osu! api
        try:
            osu_beatmapset = await ctx.osu_api_client.get_beatmapset(beatmapset_id)
        except OsuAPIRequestError as exc:
            logging.error("Failed to fetch beatmapset from osu! api: ",
                          response_code=exc.status_code, message=exc.message)
            return ServiceError.BEATMAPSETS_NOT_FOUND

        if osu_beatmapset["can_be_hyped"]:
            current_hype = osu_beatmapset["hype"]["current"]
            required_hype = osu_beatmapset["hype"]["required"]
        else:
            current_hype = 0
            required_hype = 0

        beatmapset = await repo.create(beatmapset_id=osu_beatmapset['id'],
                                       artist=osu_beatmapset['artist'],
                                       artist_unicode=osu_beatmapset['artist_unicode'],
                                       covers=osu_beatmapset['covers'],
                                       creator=osu_beatmapset['creator'],
                                       favourite_count=osu_beatmapset['favourite_count'],
                                       nsfw=osu_beatmapset['nsfw'],
                                       osu_play_count=osu_beatmapset['play_count'],
                                       preview_url=osu_beatmapset['preview_url'],
                                       source=osu_beatmapset['source'],
                                       title=osu_beatmapset['title'],
                                       title_unicode=osu_beatmapset['title_unicode'],
                                       created_by=osu_beatmapset['user_id'],
                                       video=osu_beatmapset['video'],
                                       download_disabled=osu_beatmapset['availability']['download_disabled'],
                                       availability_information=osu_beatmapset[
                                           'availability']['more_information'],
                                       bpm=osu_beatmapset['bpm'],
                                       can_be_hyped=osu_beatmapset['can_be_hyped'],
                                       discussion_locked=osu_beatmapset['discussion_locked'],
                                       current_hype=current_hype,
                                       required_hype=required_hype,
                                       is_scoreable=osu_beatmapset['is_scoreable'],
                                       legacy_thread_url=osu_beatmapset['legacy_thread_url'],
                                       current_nominations=osu_beatmapset['nominations_summary']['current'],
                                       required_nominations=osu_beatmapset['nominations_summary']['required'],
                                       ranked_status=osu_beatmapset['ranked'],
                                       storyboard=osu_beatmapset['storyboard'],
                                       tags=osu_beatmapset['tags'],
                                       osu_submitted_at=osu_beatmapset['submitted_date'].removesuffix(
                                           'Z'),
                                       osu_updated_at=osu_beatmapset['last_updated'].removesuffix(
                                           'Z'),
                                       osu_ranked_at=osu_beatmapset['ranked_date'].removesuffix(
                                           'Z'),
                                       status=Status.ACTIVE)

        if beatmapset is None:
            # return ServiceError.BEATMAPSETS_CANNOT_CREATE
            return ServiceError.BEATMAPSETS_NOT_FOUND

        # TODO: we should probably save the beatmaps from api as well?

    return beatmapset


async def fetch_many(ctx: Context, artist: str | None = None,
                     creator: str | None = None,
                     title: str | None = None,
                     nsfw: bool | None = None,
                     ranked_status: int | None = None,
                     status: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ) -> list[Mapping[str, Any]] | ServiceError:
    repo = BeatmapsetsRepo(ctx)

    beatmapsets = await repo.fetch_many(artist=artist, creator=creator,
                                        title=title, nsfw=nsfw,
                                        ranked_status=ranked_status,
                                        status=status, page=page,
                                        page_size=page_size)

    return beatmapsets


async def delete(ctx: Context, beatmapset_id: int) -> Mapping[str, Any] | ServiceError:
    repo = BeatmapsetsRepo(ctx)

    beatmapset = await repo.delete(beatmapset_id)
    if beatmapset is None:
        return ServiceError.BEATMAPSETS_NOT_FOUND

    return beatmapset
