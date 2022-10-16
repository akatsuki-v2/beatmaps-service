from enum import IntEnum
from typing import Any
from typing import Mapping

from app.common import settings
from app.common.context import Context


class BeatmapsRepo:
    # https://osu.ppy.sh/docs/index.html#beatmapcompact
    # https://osu.ppy.sh/docs/index.html#beatmap
    # TODO: how should we store osu created/updated/deleted timestamps vs. ours?
    #       combine?
    READ_PARAMS = """\
        beatmap_id, md5_hash, set_id, mode, `convert`, od, ar, cs, hp, bpm,
        hit_length, total_length, count_circles, count_sliders, count_spinners,
        difficulty_rating, is_scoreable, pass_count, play_count,
        version, created_by, ranked_status, status, created_at, updated_at
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self, beatmap_id: int, md5_hash: str, set_id: int,
                     convert: bool, mode: int, od: float, ar: float, cs: float,
                     hp: float, bpm: float, hit_length: int, total_length: int,
                     count_circles: int, count_sliders: int, count_spinners: int,
                     difficulty_rating: float, is_scoreable: bool, pass_count: int,
                     play_count: int, version: str, created_by: str,
                     ranked_status: int, status: int, deleted_at: str) -> Mapping[str, Any] | None:
        query = """\
            INSERT INTO beatmaps (
                beatmap_id, md5_hash, set_id, mode, `convert`, od, ar, cs, hp,
                bpm, hit_length, total_length, count_circles, count_sliders,
                count_spinners, difficulty_rating, is_scoreable, pass_count,
                play_count, version, created_by, ranked_status, status, deleted_at
            ) VALUES (
                :beatmap_id, :md5_hash, :set_id, :mode, :convert, :od, :ar,
                :cs, :hp, :bpm, :hit_length, :total_length, :count_circles,
                :count_sliders, :count_spinners, :difficulty_rating,
                :is_scoreable, :pass_count, :play_count, :version, :created_by,
                :ranked_status, :status, :deleted_at
            )
        """
        params = {
            "beatmap_id": beatmap_id,
            "md5_hash": md5_hash,
            "set_id": set_id,
            "mode": mode,
            "convert": convert,
            "od": od,
            "ar": ar,
            "cs": cs,
            "hp": hp,
            "bpm": bpm,
            "hit_length": hit_length,
            "total_length": total_length,
            "count_circles": count_circles,
            "count_sliders": count_sliders,
            "count_spinners": count_spinners,
            "difficulty_rating": difficulty_rating,
            "is_scoreable": is_scoreable,
            "pass_count": pass_count,
            "play_count": play_count,
            "version": version,
            "created_by": created_by,
            "ranked_status": ranked_status,
            "status": status,
            "deleted_at": deleted_at,
        }
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmaps
             WHERE beatmap_id = :beatmap_id
        """
        params = {"beatmap_id": beatmap_id}
        beatmap = await self.ctx.db.fetch_one(query, params)
        return beatmap

    async def fetch_one(self, beatmap_id: int) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmaps
             WHERE beatmap_id = :beatmap_id
        """
        params = {"beatmap_id": beatmap_id}
        beatmap = await self.ctx.db.fetch_one(query, params)
        return beatmap

    async def fetch_many(self, set_id: int | None = None,
                         mode: int | None = None,
                         ranked_status: int | None = None,
                         status: int | None = None,
                         page: int = 1,
                         page_size: int = settings.DEFAULT_PAGE_SIZE,
                         ) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmaps
             WHERE set_id = COALESCE(:set_id, set_id)
               AND mode = COALESCE(:mode, mode)
               AND ranked_status = COALESCE(:ranked_status, ranked_status)
               AND status = COALESCE(:status, status)
             LIMIT :limit
            OFFSET :offset
        """
        params = {
            "set_id": set_id,
            "mode": mode,
            "ranked_status": ranked_status,
            "status": status,
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }
        beatmaps = await self.ctx.db.fetch_all(query, params)
        return beatmaps

    # TODO: fetch_count for pagination metadata?

    async def partial_update(self, beatmap_id: int, **kwargs: Any
                             ) -> Mapping[str, Any] | None:
        # TODO: use null coalescence to update fields
        query = """\
            UPDATE beatmaps
               SET {}
             WHERE beatmap_id = :beatmap_id
        """.format(", ".join(f"{k} = :{k}" for k in kwargs))
        params = {"beatmap_id": beatmap_id, **kwargs}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmaps
             WHERE beatmap_id = :beatmap_id
        """
        params = {"beatmap_id": beatmap_id}
        beatmap = await self.ctx.db.fetch_one(query, params)
        return beatmap

    async def delete(self, beatmap_id: int) -> Mapping[str, Any] | None:
        query = """\
            DELETE FROM beatmaps
             WHERE beatmap_id = :beatmap_id
        """
        params = {"beatmap_id": beatmap_id}
        await self.ctx.db.execute(query, params)

        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM beatmaps
             WHERE beatmap_id = :beatmap_id
        """
        params = {"beatmap_id": beatmap_id}
        beatmap = await self.ctx.db.fetch_one(query, params)
        return beatmap
