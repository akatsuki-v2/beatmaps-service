from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    BEATMAPS_CANNOT_CREATE = "beatmaps.cannot_create"
    BEATMAPS_CANNOT_UPDATE = "beatmaps.cannot_update"
    BEATMAPS_CANNOT_DELETE = "beatmaps.cannot_delete"
    BEATMAPS_NOT_FOUND = "beatmaps.not_found"

    BEATMAPSETS_CANNOT_CREATE = "beatmapsets.cannot_create"
    BEATMAPSETS_CANNOT_UPDATE = "beatmapsets.cannot_update"
    BEATMAPSETS_CANNOT_DELETE = "beatmapsets.cannot_delete"
    BEATMAPSETS_NOT_FOUND = "beatmapsets.not_found"
