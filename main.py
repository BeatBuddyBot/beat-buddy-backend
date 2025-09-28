from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.playlists.router import playlists_router
from src.songs.router import songs_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(playlists_router)
app.include_router(songs_router)
