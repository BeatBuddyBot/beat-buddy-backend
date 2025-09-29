from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.songs.schemas import SongResponse


class PlaylistCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None


class PlaylistPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    is_favourite: Optional[bool] = None


class PlaylistResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    cover_url: Optional[str]
    duration: int
    length: int
    is_favourite: bool


class PlaylistWithSongsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    cover_url: Optional[str]
    duration: int
    length: int
    is_favourite: bool
    songs: list[SongResponse]
