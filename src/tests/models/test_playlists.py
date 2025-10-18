import os
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from src.playlists.models import Playlist
from src.playlists.utils import upload_cover


class TestPlaylistModel:

    def test_playlist_model_creation(self, test_session):
        playlist = Playlist(title="Test Model Playlist", description="Test description")

        test_session.add(playlist)
        test_session.commit()
        test_session.refresh(playlist)

        assert playlist.id is not None
        assert playlist.title == "Test Model Playlist"
        assert playlist.description == "Test description"
        assert playlist.is_favorite is False
        assert playlist.created_at is not None
        assert playlist.cover_key is None

    def test_duration_property_and_consistency_python_vs_orm(
        self, test_session, make_playlist, make_song
    ):
        playlist = make_playlist()

        make_song(playlist, duration=100)
        make_song(playlist, duration=200)
        make_song(playlist, duration=150)

        # Python level
        python_duration = playlist.duration

        # ORM level
        orm_duration = test_session.execute(
            select(Playlist.duration).where(Playlist.id == playlist.id)
        ).scalar()

        assert python_duration == orm_duration == 450

    def test_length_property_and_consistency_python_vs_orm(
        self, test_session, make_playlist, make_song
    ):
        playlist = make_playlist()

        make_song(playlist)
        make_song(playlist)
        make_song(playlist)
        make_song(playlist)

        # Python level
        python_length = playlist.length

        # ORM level
        orm_length = test_session.execute(
            select(Playlist.length).where(Playlist.id == playlist.id)
        ).scalar()

        assert python_length == orm_length == 4

    def test_upload_cover_valid_base64_png(
        self, mock_s3_client_put, sample_image_base64
    ):
        result = upload_cover(sample_image_base64)

        # Verify S3 client was called
        mock_s3_client_put.assert_called_once()

        call_args = mock_s3_client_put.call_args
        assert call_args[1]["Bucket"] == os.getenv("AWS_BUCKET_NAME")
        assert call_args[1]["Key"].startswith("covers/")
        assert call_args[1]["ContentType"] == "image/png"

        assert result == call_args[1]["Key"]

    def test_upload_cover_invalid_base64_format(self):
        with pytest.raises(HTTPException) as exc_info:
            upload_cover("invalid_base64_string")

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert exc_info.value.detail == "Incorrect base64"

    def test_playlist_without_cover_image(self, make_playlist):
        playlist = make_playlist()

        assert playlist.cover_key is None
        assert playlist.cover_url is None
