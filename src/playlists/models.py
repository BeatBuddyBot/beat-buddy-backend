from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from src.models import Base


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    cover_key = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.utc_timestamp())
    songs = relationship("Song", backref="playlist", cascade="all")
