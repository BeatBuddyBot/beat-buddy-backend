import json

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.player.schemas import PlayerAddSong, PlayerAddPlaylist
from src.player.utils import redis_client
from src.songs.models import Song

player_router = APIRouter(prefix="/player", tags=["player"])


@player_router.post("/add/song/", status_code=204)
def play(song_data: PlayerAddSong):
    redis_client.publish(
        "bot_player",
        json.dumps({"action": "play", "urls": [song_data.url]}),
    )


@player_router.post("/add/playlist/", status_code=204)
def play(playlist_data: PlayerAddPlaylist, session: Session = Depends(get_session)):
    query = select(Song.url).where(Song.playlist_id == playlist_data.playlist_id)
    urls = session.execute(query).scalars().all()
    redis_client.publish(
        "bot_player",
        json.dumps({"action": "play", "urls": urls}),
    )


@player_router.post("/stop/", status_code=204)
def stop():
    redis_client.publish("bot_player", json.dumps({"action": "stop"}))


@player_router.post("/pause/", status_code=204)
def pause():
    redis_client.publish("bot_player", json.dumps({"action": "pause"}))


@player_router.post("/skip/", status_code=204)
def skip():
    redis_client.publish("bot_player", json.dumps({"action": "skip"}))


@player_router.post("/repeat/", status_code=204)
def repeat():
    redis_client.publish("bot_player", json.dumps({"action": "repeat"}))
