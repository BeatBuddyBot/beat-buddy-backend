from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database import get_session
from src.playlists.models import Playlist
from src.songs.models import Song
from src.songs.schemas import SongResponse, SongCreate

songs_router = APIRouter(prefix="/songs", tags=["songs"])


@songs_router.post("/", response_model=SongResponse)
def create_song(song_data: SongCreate, session: Session = Depends(get_session)):
    playlist = session.get(Playlist, song_data.playlist_id)

    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    song = Song(**song_data.model_dump())
    session.add(song)
    session.commit()
    return song


@songs_router.delete("/{song_id}/", status_code=204)
def delete_song(song_id: int, session: Session = Depends(get_session)):
    song = session.get(Song, song_id)

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    session.delete(song)
    session.commit()
