from app.models import BaseModel


class BeatmapInput(BaseModel):
    beatmap_id: int
    md5_hash: str
    set_id: int
    convert: bool
    mode: int
    od: float
    ar: float
    cs: float
    hp: float
    bpm: float
    hit_length: int
    total_length: int
    count_circles: int
    count_sliders: int
    count_spinners: int
    difficulty_rating: float
    is_scorable: bool
    pass_count: int
    play_count: int
    version: str
    created_by: str
    ranked_status: int
    status: int
    created_at: str
    updated_at: str
    deleted_at: str


class Beatmap(BaseModel):
    beatmap_id: int
    md5_hash: str
    set_id: int
    convert: bool
    mode: int
    od: float
    ar: float
    cs: float
    hp: float
    bpm: float
    hit_length: int
    total_length: int
    count_circles: int
    count_sliders: int
    count_spinners: int
    difficulty_rating: float
    is_scorable: bool
    pass_count: int
    play_count: int
    version: str
    created_by: str
    ranked_status: int
    status: int
    created_at: str
    updated_at: str
    deleted_at: str


# TODO: think more about whether we want our initial impl to support custom maps
class BeatmapUpdate(BaseModel):
    ...
