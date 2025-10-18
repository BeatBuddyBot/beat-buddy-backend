from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SongCreate(BaseModel):
    url: str
    title: str
    duration: int
    playlist_id: int


class SongPatch(BaseModel):
    position: int


class SongResponse(BaseModel):
    id: int
    title: str
    url: str
    created_at: datetime
    updated_at: Optional[datetime]
    position: int
    duration: int
    playlist_id: int
