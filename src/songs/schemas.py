from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class SongCreate(BaseModel):
    url: str
    title: str
    duration: int
    playlist_id: int


class SongResponse(BaseModel):
    id: int
    title: str
    url: str
    created_at: datetime
    updated_at: Optional[datetime]
    position: int
    duration: int
    playlist_id: int
