import os
from unittest.mock import MagicMock

import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import src.aws.client
from src.database import get_session, TEST_DB_URL
from main import app
from src.playlists.models import Playlist

@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(TEST_DB_URL)

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    yield engine

    command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="function")
def test_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_session):
    def override_get_session():
        try:
            yield test_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_s3_client_put(monkeypatch):
    """
       Automatically mocks the `put_object` method of the S3 client for tests.
    """
    mock_put = MagicMock()
    monkeypatch.setattr(src.aws.client.s3_client, "put_object", mock_put)
    yield mock_put

@pytest.fixture
def sample_image_base64():
    os.getcwd()
    path = "src/tests/resources/image_base64.txt"
    with open(path, "r") as f:
        return f.read().strip()


@pytest.fixture
def make_playlist(test_session):
    def _make_playlist(title="Test Playlist", description="A test playlist", is_favorite=False):
        playlist = Playlist(
            title=title,
            description=description,
            is_favorite=is_favorite
        )
        test_session.add(playlist)
        test_session.commit()
        test_session.refresh(playlist)
        return playlist

    return _make_playlist
