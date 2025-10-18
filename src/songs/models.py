from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    event,
    func,
    select,
)

from src.models import Base


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_onupdate=func.utc_timestamp())
    playlist_id = Column(ForeignKey("playlists.id"))


@event.listens_for(Song, "before_insert")
def set_song_position(mapper, connection, target):
    if target.position is not None:
        return

    max_position = connection.execute(
        select(func.max(Song.position)).where(Song.playlist_id == target.playlist_id)
    ).scalar()
    target.position = 1 if max_position is None else max_position + 1
