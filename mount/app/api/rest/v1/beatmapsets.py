from app.api.rest.context import RequestContext
from app.common import responses
from app.common import settings
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.beatmapsets import Beatmapset
from app.models.beatmapsets import BeatmapsetInput
from app.usecases import beatmapsets
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/beatmapsets", response_model=Success[Beatmapset])
async def create(args: BeatmapsetInput, ctx: RequestContext = Depends()):
    data = await beatmapsets.create(ctx,
                                    beatmapset_id=args.beatmapset_id,
                                    artist=args.artist,
                                    artist_unicode=args.artist_unicode,
                                    covers=args.covers,
                                    creator=args.creator,
                                    favourite_count=args.favourite_count,
                                    nsfw=args.nsfw,
                                    osu_play_count=args.osu_play_count,
                                    preview_url=args.preview_url,
                                    source=args.source,
                                    title=args.title,
                                    title_unicode=args.title_unicode,
                                    mapper_id=args.mapper_id,
                                    mapper_name=args.mapper_name,
                                    video=args.video,
                                    download_disabled=args.download_disabled,
                                    availability_information=args.availability_information,
                                    bpm=args.bpm,
                                    can_be_hyped=args.can_be_hyped,
                                    discussion_locked=args.discussion_locked,
                                    current_hype=args.current_hype,
                                    required_hype=args.required_hype,
                                    is_scoreable=args.is_scoreable,
                                    legacy_thread_url=args.legacy_thread_url,
                                    current_nominations=args.current_nominations,
                                    required_nominations=args.required_nominations,
                                    ranked_status=args.ranked_status,
                                    storyboard=args.storyboard,
                                    tags=args.tags,
                                    osu_submitted_at=args.osu_submitted_at,
                                    osu_updated_at=args.osu_updated_at,
                                    osu_ranked_at=args.osu_ranked_at)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create beatmapset")

    resp = Beatmapset.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/beatmapsets/{beatmapset_id}", response_model=Success[Beatmapset])
async def fetch_one(beatmapset_id: int, ctx: RequestContext = Depends()):
    data = await beatmapsets.fetch_one(ctx, beatmapset_id=beatmapset_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch beatmapset")

    resp = Beatmapset.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/beatmapsets", response_model=Success[list[Beatmapset]])
async def fetch_many(artist: str | None = None,
                     creator: str | None = None,
                     title: str | None = None,
                     nsfw: bool | None = None,
                     ranked_status: int | None = None,
                     status: str | None = None,
                     page: int = 1,
                     page_size: int = settings.DEFAULT_PAGE_SIZE,
                     ctx: RequestContext = Depends()):
    data = await beatmapsets.fetch_many(ctx, artist=artist, creator=creator,
                                        title=title, nsfw=nsfw,
                                        ranked_status=ranked_status,
                                        status=status,
                                        page=page,
                                        page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch beatmapsets")

    resp = [Beatmapset.from_mapping(rec) for rec in data]
    return responses.success(resp)


# TODO: partial_update


@router.delete("/v1/beatmapsets/{beatmapset_id}", response_model=Success[Beatmapset])
async def delete(beatmapset_id: int, ctx: RequestContext = Depends()):
    data = await beatmapsets.delete(ctx, beatmapset_id=beatmapset_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete beatmapset")

    resp = Beatmapset.from_mapping(data)
    return responses.success(resp)
