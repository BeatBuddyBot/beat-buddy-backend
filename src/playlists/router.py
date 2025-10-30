from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import nulls_last
from sqlalchemy.orm import Session, selectinload
from starlette import status

from src.database import get_session
from src.playlists.models import Playlist
from src.playlists.schemas import (
    PlaylistCreate,
    PlaylistPatch,
    PlaylistResponse,
    PlaylistWithSongsResponse,
)
from src.playlists.utils import upload_cover

playlists_router = APIRouter(prefix="/playlists", tags=["playlists"])


@playlists_router.post(
    "/", response_model=PlaylistResponse, status_code=status.HTTP_201_CREATED
)
def create_playlist(
    playlist_data: PlaylistCreate, session: Session = Depends(get_session)
):
    playlist = Playlist(**playlist_data.model_dump(exclude={"cover_image"}))

    if playlist_data.cover_image:
        cover_key = upload_cover(playlist_data.cover_image)
        playlist.cover_key = cover_key

    session.add(playlist)
    session.commit()
    return playlist


@playlists_router.get("/", response_model=list[PlaylistResponse])
def get_playlists(session: Session = Depends(get_session)):
    playlists = (
        session.query(Playlist)
        .options(selectinload(Playlist.songs))
        .order_by(Playlist.is_favorite.desc(), nulls_last(Playlist.created_at.desc()))
        .all()
    )
    return playlists


@playlists_router.get("/{playlist_id}/", response_model=PlaylistWithSongsResponse)
def get_playlist(playlist_id: int, session: Session = Depends(get_session)):
    playlist = (
        session.query(Playlist)
        .options(selectinload(Playlist.songs))
        .filter(Playlist.id == playlist_id)
        .first()
    )

    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    return playlist


@playlists_router.patch("/{playlist_id}/", response_model=PlaylistResponse)
def patch_playlist(
    playlist_id: int,
    playlist_data: PlaylistPatch,
    session: Session = Depends(get_session),
):
    playlist = session.get(Playlist, playlist_id)

    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    for var, value in playlist_data.model_dump(
        exclude_unset=True, exclude={"cover_image"}
    ).items():
        setattr(playlist, var, value)

    if playlist_data.cover_image:
        cover_key = upload_cover(playlist_data.cover_image)
        playlist.cover_key = cover_key

    session.commit()
    session.refresh(playlist)
    return playlist


@playlists_router.delete("/{playlist_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(playlist_id: int, session: Session = Depends(get_session)):
    playlist = session.get(Playlist, playlist_id)

    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found"
        )

    session.delete(playlist)
    session.commit()
