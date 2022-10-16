from app.api.rest.context import RequestContext
from app.common import responses
from app.common import settings
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.beatmaps import Beatmap
from app.models.beatmaps import BeatmapInput
from app.usecases import beatmaps
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/beatmaps", response_model=Success[Beatmap])
async def create(args: BeatmapInput, ctx: RequestContext = Depends()):
    data = await beatmaps.create(ctx, beatmap_id=args.beatmap_id,
                                 md5_hash=args.md5_hash,
                                 set_id=args.set_id,
                                 convert=args.convert,
                                 mode=args.mode,
                                 od=args.od,
                                 ar=args.ar,
                                 cs=args.cs,
                                 hp=args.hp,
                                 bpm=args.bpm,
                                 hit_length=args.hit_length,
                                 total_length=args.total_length,
                                 count_circles=args.count_circles,
                                 count_sliders=args.count_sliders,
                                 count_spinners=args.count_spinners,
                                 difficulty_rating=args.difficulty_rating,
                                 is_scorable=args.is_scorable,
                                 pass_count=args.pass_count,
                                 play_count=args.play_count,
                                 version=args.version,
                                 created_by=args.created_by,
                                 ranked_status=args.ranked_status,
                                 status=args.status,
                                 created_at=args.created_at,
                                 updated_at=args.updated_at,
                                 deleted_at=args.deleted_at)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create beatmap")

    resp = Beatmap.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/beatmaps/{beatmap_id}", response_model=Success[Beatmap])
async def fetch_one(beatmap_id: int, ctx: RequestContext = Depends()):
    data = await beatmaps.fetch_one(ctx, beatmap_id=beatmap_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch beatmap")

    resp = Beatmap.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/beatmaps", response_model=Success[list[Beatmap]])
async def fetch_many(set_id: int | None = None,
                     mode: int | None = None,
                     ranked_status: int | None = None,
                     status: int | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ctx: RequestContext = Depends()):
    data = await beatmaps.fetch_many(ctx, set_id=set_id,
                                     mode=mode,
                                     ranked_status=ranked_status,
                                     status=status,
                                     page=page,
                                     page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch beatmaps")

    resp = [Beatmap.from_mapping(rec) for rec in data]
    return responses.success(resp)


# TODO: partial_update


@router.delete("/v1/beatmaps/{beatmap_id}", response_model=Success[Beatmap])
async def delete(beatmap_id: int, ctx: RequestContext = Depends()):
    data = await beatmaps.delete(ctx, beatmap_id=beatmap_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete beatmap")

    resp = Beatmap.from_mapping(data)
    return responses.success(resp)
