from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.songs.schemas import SongResponse


class PlaylistCreate(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image: Optional[str] = None


class PlaylistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None


class PlaylistResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    cover_key: Optional[str]


class PlaylistWithSongsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    songs: list[SongResponse]
