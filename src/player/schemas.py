from typing import Optional

from pydantic import BaseModel


class PlayerAddSong(BaseModel):
    url: Optional[str]


class PlayerAddPlaylist(BaseModel):
    playlist_id: Optional[int]
