from typing import Optional

from pydantic import BaseModel


class PlayerStartSong(BaseModel):
    url: Optional[str]


class PlayerStartPlaylist(BaseModel):
    playlist_id: Optional[int]
