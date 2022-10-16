from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    BEATMAPS_CANNOT_CREATE = "beatmaps.cannot_create"
    BEATMAPS_CANNOT_UPDATE = "beatmaps.cannot_update"
    BEATMAPS_CANNOT_DELETE = "beatmaps.cannot_delete"
    BEATMAPS_NOT_FOUND = "beatmaps.not_found"
