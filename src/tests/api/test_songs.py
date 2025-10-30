from starlette import status


class TestSongsAPI:

    def test_create_song(self, client, make_playlist):
        playlist = make_playlist()

        song_data = {
            "url": "https://youtu.be/UbQgXeY_zi4",
            "title": "Caravan Palace - Lone Digger (Official MV)",
            "duration": 170,
            "playlist_id": playlist.id,
        }

        response = client.post("/api/v1/songs/", json=song_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["title"] == song_data["title"]
        assert data["url"] == song_data["url"]
        assert data["duration"] == song_data["duration"]
        assert data["playlist_id"] == playlist.id
        assert data["position"] == 0
        assert data["id"] is not None
        assert data["created_at"] is not None

    def test_create_song_invalid_data(self, client, make_playlist):
        song_data = {
            "title": "Caravan Palace - Lone Digger (Official MV)",
        }

        response = client.post("/api/v1/songs/", json=song_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_song_invalid_playlist(self, client):
        song_data = {
            "url": "https://youtu.be/UbQgXeY_zi4",
            "title": "Caravan Palace - Lone Digger (Official MV)",
            "duration": 170,
            "playlist_id": 999,  # Non-existent playlist
        }

        response = client.post("/api/v1/songs/", json=song_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Playlist not found"

    def test_patch_song_position(self, client, make_playlist, make_song, test_session):
        playlist = make_playlist()
        song1 = make_song(playlist=playlist)
        song2 = make_song(playlist=playlist)

        response = client.patch(f"/api/v1/songs/{song1.id}/", json={"position": 1})
        assert response.status_code == status.HTTP_200_OK

        test_session.refresh(song1)
        test_session.refresh(song2)

        assert song1.position == 1
        assert song2.position == 0

    def test_patch_song_not_found(self, client):
        response = client.patch("/api/v1/songs/999/", json={"position": 1})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Song not found"

    def test_delete_song(self, client, make_song, test_session):
        song = make_song()
        song_id = song.id
        response = client.delete(f"/api/v1/songs/{song_id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify song is deleted by trying to patch it
        patch_response = client.patch(f"/api/v1/songs/{song_id}/", json={"position": 1})
        assert patch_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_song_not_found(self, client):
        response = client.delete("/api/v1/songs/999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Song not found"
