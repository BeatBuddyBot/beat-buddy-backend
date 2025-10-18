from src.playlists.models import Playlist


class TestPlaylistModel:

    def test_playlist_model_creation(self, test_session):
        playlist = Playlist(
            title="Test Model Playlist",
            description="Test description"
        )

        test_session.add(playlist)
        test_session.commit()
        test_session.refresh(playlist)

        assert playlist.id is not None
        assert playlist.title == "Test Model Playlist"
        assert playlist.description == "Test description"
        assert playlist.is_favorite is False
        assert playlist.created_at is not None
        assert playlist.cover_key is None

    def test_cover_url_is_none_when_cover_key_is_null(self, make_playlist):
        playlist1 = make_playlist(cover_key=None)
        assert playlist1.cover_url is None

        playlist2 = make_playlist(cover_key='some_key')
        assert playlist2.cover_key is not None

    def test_playlist_length(self, test_session, make_playlist, make_song):
        playlist = make_playlist()
        assert playlist.length == 0

        make_song(playlist)
        make_song(playlist)
        make_song(playlist)

        assert playlist.length == 3

    def test_playlist_duration(self, test_session, make_playlist, make_song):
        playlist = make_playlist()
        assert playlist.duration == 0

        make_song(playlist, duration=150)
        make_song(playlist, duration=100)
        make_song(playlist, duration=200)

        assert playlist.duration == 450
