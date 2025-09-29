import os
from functools import cached_property

from sqlalchemy import Column, Integer, String, DateTime, func, select, Boolean, text
from sqlalchemy.ext.hybrid import hybrid_property
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
    is_favourite = Column(Boolean, nullable=False, server_default=text("false"))
    songs = relationship("Song", backref="playlist", cascade="all")

    @cached_property
    def bucket_domain(self):
        return f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com"

    @hybrid_property
    def cover_url(self):
        if self.cover_key:
            return f"{self.bucket_domain}/{self.cover_key}"
        return None
    
    @hybrid_property
    def duration(self):
        return sum(song.duration for song in self.songs)

    @duration.expression
    def duration(self):
        from src.songs.models import Song
        return select(func.coalesce(func.sum(Song.duration), 0)).where(
            Song.playlist_id == self.id
        ).scalar_subquery()

    @hybrid_property
    def length(self):
        return len(self.songs)

    @length.expression
    def length(self):
        from src.songs.models import Song
        return (
            select(func.count(Song.id))
            .where(Song.playlist_id == self.id)
            .scalar_subquery()
        )
