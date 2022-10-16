from __future__ import annotations

from fastapi import APIRouter

from . import beatmaps

router = APIRouter()

router.include_router(beatmaps.router, tags=["beatmaps"])
