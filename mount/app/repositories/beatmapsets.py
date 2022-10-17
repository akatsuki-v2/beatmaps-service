from datetime import datetime
from typing import Any
from typing import Mapping

from app.common import json
from app.common import settings
from app.common.context import Context


class BeatmapsetsRepo:
    # https://osu.ppy.sh/docs/index.html#beatmapsetcompact
    # https://osu.ppy.sh/docs/index.html#beatmapset
    READ_PARAMS = """\
        beatmapset_id, artist, artist_unicode, covers, creator, favourite_count,
        nsfw, osu_play_count, preview_url, source, title, title_unicode,
        created_by, video, download_disabled, availability_information, bpm,
        can_be_hyped, discussion_locked, current_hype, required_hype,
        is_scoreable, legacy_thread_url, current_nominations,
        required_nominations, ranked_status, storyboard,
        osu_submitted_at, osu_updated_at, osu_ranked_at,
        tags, status, created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, beatmapset_id: int, artist: str, artist_unicode: str,
                     covers: dict[str, Any], creator: str, favourite_count: int,
                     nsfw: bool, osu_play_count: int, preview_url: str,
                     source: str, title: str, title_unicode: str,
                     created_by: int, video: bool, download_disabled: bool,
                     availability_information: str | None, bpm: float,
                     can_be_hyped: bool, discussion_locked: bool,
                     current_hype: int, required_hype: int, is_scoreable: bool,
                     legacy_thread_url: str,
                     current_nominations: int, required_nominations: int,
                     ranked_status: int, storyboard: bool, tags: str,
                     osu_submitted_at: datetime, osu_updated_at: datetime,
                     osu_ranked_at: datetime | None, status: str
                     ) -> Mapping[str, Any] | None:
        query = """\
            INSERT INTO beatmapsets (
                beatmapset_id, artist, artist_unicode, covers, creator,
                favourite_count, nsfw, osu_play_count, preview_url, source,
                title, title_unicode, created_by, video, download_disabled,
                availability_information, bpm, can_be_hyped, discussion_locked,
                current_hype, required_hype, is_scoreable,
                legacy_thread_url, current_nominations, required_nominations,
                ranked_status, storyboard, tags, osu_submitted_at,
                osu_updated_at, osu_ranked_at, status
            ) VALUES (
                :beatmapset_id, :artist, :artist_unicode, :covers, :creator,
                :favourite_count, :nsfw, :osu_play_count, :preview_url, :source,
                :title, :title_unicode, :created_by, :video, :download_disabled,
                :availability_information, :bpm, :can_be_hyped,
                :discussion_locked, :current_hype, :required_hype,
                :is_scoreable, :legacy_thread_url,
                :current_nominations, :required_nominations, :ranked_status,
                :storyboard, :tags, :osu_submitted_at, :osu_updated_at,
                :osu_ranked_at, :status
            )
        """
        params = {
            "beatmapset_id": beatmapset_id,
            "artist": artist,
            "artist_unicode": artist_unicode,
            "covers": json.dumps(covers).decode(),
            "creator": creator,
            "favourite_count": favourite_count,
            "nsfw": nsfw,
            "osu_play_count": osu_play_count,
            "preview_url": preview_url,
            "source": source,
            "title": title,
            "title_unicode": title_unicode,
            "created_by": created_by,
            "video": video,
            "download_disabled": download_disabled,
            "availability_information": availability_information,
            "bpm": bpm,
            "can_be_hyped": can_be_hyped,
            "discussion_locked": discussion_locked,
            "current_hype": current_hype,
            "required_hype": required_hype,
            "is_scoreable": is_scoreable,
            "legacy_thread_url": legacy_thread_url,
            "current_nominations": current_nominations,
            "required_nominations": required_nominations,
            "ranked_status": ranked_status,
            "storyboard": storyboard,
            "tags": tags,
            "osu_submitted_at": osu_submitted_at,
            "osu_updated_at": osu_updated_at,
            "osu_ranked_at": osu_ranked_at,
            "status": status,
        }
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmapsets
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id}
        beatmapset = await self.ctx.db.fetch_one(query, params)
        return beatmapset

    async def fetch_one(self, beatmapset_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmapsets
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id}
        beatmapset = await self.ctx.db.fetch_one(query, params)
        return beatmapset

    async def fetch_many(self, artist: str | None = None,
                         creator: str | None = None,
                         title: str | None = None,
                         nsfw: bool | None = None,
                         ranked_status: int | None = None,
                         status: str | None = None,
                         page: int = 1,
                         page_size: int = settings.DEFAULT_PAGE_SIZE,
                         ) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmapsets
             WHERE artist = COALESCE(:artist, artist)
               AND creator = COALESCE(:creator, creator)
               AND title = COALESCE(:title, title)
               AND nsfw = COALESCE(:nsfw, nsfw)
               AND ranked_status = COALESCE(:ranked_status, ranked_status)
               AND status = COALESCE(:status, status)
             LIMIT :limit
            OFFSET :offset
        """
        params = {
            "artist": artist,
            "creator": creator,
            "title": title,
            "nsfw": nsfw,
            "ranked_status": ranked_status,
            "status": status,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }
        beatmapsets = await self.ctx.db.fetch_all(query, params)
        return beatmapsets

    # TODO: fetch_count for pagination metadata?

    async def partial_update(self, beatmapset_id: int, **kwargs: Any
                             ) -> Mapping[str, Any] | None:
        # TODO: use null coalescence to update fields
        query = f"""\
            UPDATE beatmapsets
               SET {", ".join(f"{k} = :{k}" for k in kwargs)}
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id, **kwargs}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmapsets
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id}
        beatmapset = await self.ctx.db.fetch_one(query, params)
        return beatmapset

    async def delete(self, beatmapset_id: int) -> Mapping[str, Any] | None:
        query = """\
            UPDATE beatmapsets
               SET status = 'deleted',
                   updated_at = NOW()
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmapsets
             WHERE beatmapset_id = :beatmapset_id
        """
        params = {"beatmapset_id": beatmapset_id}
        beatmapset = await self.ctx.db.fetch_one(query, params)
        return beatmapset
