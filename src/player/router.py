import asyncio
import json

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.player.schemas import PlayerStartPlaylist, PlayerStartSong
from src.player.utils import redis_client
from src.songs.models import Song

player_router = APIRouter(prefix="/player", tags=["player"])


@player_router.websocket("/status_stream")
async def status_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        mock = {
            "is_playing": True,
            "player": {
                "paused": False,
                "repeat": "disabled",
                "current_song": {
                    "title": "УННВ - Без даты (Remix)",
                    "duration": 240000,
                    "elapsed": 120000
                }
            },
            "queue": [
                {
                    "title": "голубые глазки",
                    "duration": "180000"
                },
                {
                    "title": "киси-киси мяу-мяу",
                    "duration": "180000"
                },
                {
                    "title": "GHOST! - phonk.me & KIIXSHI",
                    "duration": "200000"
                },
                {
                    "title": "Microwave Edit Song (Slowed)",
                    "duration": "150000"
                }
            ]
        }
        await websocket.send_json(mock)
        await asyncio.sleep(1)


@player_router.post("/start/song", status_code=204)
def start_song(song_data: PlayerStartSong):
    redis_client.publish(
        "bot_player",
        json.dumps({"action": "play", "urls": [song_data.url]}),
    )


@player_router.post("/start/playlist", status_code=204)
def start_playlist(
        playlist_data: PlayerStartPlaylist, session: Session = Depends(get_session)
):
    query = (
        select(Song.url)
        .where(Song.playlist_id == playlist_data.playlist_id)
        .order_by(Song.position)
    )
    urls = session.execute(query).scalars().all()
    redis_client.publish(
        "bot_player",
        json.dumps({"action": "play", "urls": urls}),
    )


@player_router.post("/stop", status_code=204)
def stop():
    redis_client.publish("bot_player", json.dumps({"action": "stop"}))


@player_router.post("/pause", status_code=204)
def pause():
    redis_client.publish("bot_player", json.dumps({"action": "pause"}))


@player_router.post("/skip", status_code=204)
def skip():
    redis_client.publish("bot_player", json.dumps({"action": "skip"}))


@player_router.post("/repeat", status_code=204)
def repeat():
    redis_client.publish("bot_player", json.dumps({"action": "repeat"}))
