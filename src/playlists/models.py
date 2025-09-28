import os
from functools import cached_property

from sqlalchemy import Column, Integer, String, DateTime, func
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
    songs = relationship("Song", backref="playlist", cascade="all")

    @cached_property
    def bucket_domain(self):
        return f"https://{os.getenv('AWS_BUCKET_NAME')}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com"

    @hybrid_property
    def cover_url(self):
        if self.cover_key:
            return f"{self.bucket_domain}/{self.cover_key}"
        return None
