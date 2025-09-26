from fastapi import FastAPI

from src.playlists.router import playlists_router
from src.songs.router import songs_router

app = FastAPI()
app.include_router(playlists_router)
app.include_router(songs_router)
