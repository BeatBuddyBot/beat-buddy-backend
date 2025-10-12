from typing import Optional, Literal

from pydantic import BaseModel


class PlayerPlay(BaseModel):
    type: Literal["playlist", "url"]
    playlist_id: Optional[int] = None
    url: Optional[str] = None
