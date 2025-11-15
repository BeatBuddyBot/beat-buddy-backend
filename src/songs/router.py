from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database import get_session
from src.playlists.models import Playlist
from src.songs.models import Song
from src.songs.schemas import SongCreate, SongPatch, SongResponse

songs_router = APIRouter(prefix="/songs", tags=["songs"])


@songs_router.post(
    "/", response_model=SongResponse, status_code=status.HTTP_201_CREATED
)
def create_song(song_data: SongCreate, session: Session = Depends(get_session)):
    playlist = session.get(Playlist, song_data.playlist_id)

    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    song = Song(**song_data.model_dump())
    session.add(song)
    session.commit()
    return song


@songs_router.patch("/{song_id}/", response_model=SongResponse)
def patch_song(
    song_id: int, song_data: SongPatch, session: Session = Depends(get_session)
):
    song = session.get(Song, song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Song not found"
        )

    for var, value in song_data.model_dump().items():
        setattr(song, var, value)

    session.commit()
    session.refresh(song)
    return song


@songs_router.delete("/{song_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_song(song_id: int, session: Session = Depends(get_session)):
    song = session.get(Song, song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Song not found"
        )

    session.delete(song)
    session.commit()
