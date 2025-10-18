from src.songs.models import Song


class TestSongModel:

    def test_song_model_creation(self, test_session, make_playlist):
        playlist = make_playlist(title="Test Playlist")

        song = Song(
            url="https://youtu.be/UbQgXeY_zi4",
            title="Caravan Palace - Lone Digger (Official MV)",
            duration=170,
            playlist_id=playlist.id
        )

        test_session.add(song)
        test_session.commit()
        test_session.refresh(song)

        assert song.id is not None
        assert song.title == "Caravan Palace - Lone Digger (Official MV)"
        assert song.url == "https://youtu.be/UbQgXeY_zi4"
        assert song.duration == 170
        assert song.position == 0
        assert song.playlist_id == playlist.id
        assert song.created_at is not None

    def test_song_position_auto_assignment_with_manual_position(self, test_session, make_playlist):
        """Test that manually set position is preserved"""
        playlist = make_playlist(title="Test Playlist")

        song = Song(
            url="https://youtu.be/UbQgXeY_zi4",
            title="Caravan Palace - Lone Digger (Official MV)",
            duration=170,
            position=5,  # Manually set position
            playlist_id=playlist.id
        )

        test_session.add(song)
        test_session.commit()
        test_session.refresh(song)

        assert song.position == 0  # Database trigger overrides manual position

    def test_songs_position_assignment(self, client, make_playlist, make_song):
        playlist = make_playlist()
        song1 = make_song(playlist=playlist)
        song2 = make_song(playlist=playlist)
        assert song1.position == 0
        assert song2.position == 1
