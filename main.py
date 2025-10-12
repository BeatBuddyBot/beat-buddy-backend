from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.player.router import player_router
from src.playlists.router import playlists_router
from src.songs.router import songs_router

app = FastAPI()
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(playlists_router)
api_router.include_router(songs_router)
api_router.include_router(player_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
