from starlette import status


class TestPlaylistsAPI:

    def test_create_playlist(self, client):
        sample_playlist_data = {
            "title": "Test Playlist",
            "description": "A test playlist for unit testing",
            "cover_image": None
        }
        response = client.post("/api/v1/playlists/", json=sample_playlist_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["title"] == sample_playlist_data["title"]
        assert data["description"] == sample_playlist_data["description"]
        assert data["id"] is not None
        assert data["created_at"] is not None
        assert data["is_favorite"] is False
        assert data["duration"] == 0
        assert data["length"] == 0

    def test_create_empty_playlist(self, client):
        minimal_data = {}
        response = client.post("/api/v1/playlists/", json=minimal_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "New Playlist #1"

    def test_get_playlists(self, client, make_playlist):
        make_playlist()

        response = client.get("/api/v1/playlists/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_playlists_ordering(self, client, make_playlist):
        """ Favorites first, then by created_at"""
        playlist1 = make_playlist(title="First Playlist")
        playlist2 = make_playlist(title="Second Playlist", is_favorite=True)
        playlist3 = make_playlist(title="Third Playlist")

        response = client.get("/api/v1/playlists/")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        assert len(data) == 3
        assert data[0]["title"] == "Second Playlist"
        assert data[1]["title"] == "Third Playlist"
        assert data[2]["title"] == "First Playlist"

    def test_get_playlist(self, client, make_playlist):
        playlist = make_playlist()
        response = client.get(f"/api/v1/playlists/{playlist.id}/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == playlist.id
        assert data["title"] == playlist.title

    def test_get_playlist_not_found(self, client):
        response = client.get("/api/v1/playlists/999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_playlist_success(self, client, make_playlist):
        playlist = make_playlist()
        print(playlist.is_favorite)

        response = client.patch(f"/api/v1/playlists/{playlist.id}/", json={"is_favorite": True})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_favorite"] == playlist.is_favorite == True

    def test_update_playlist_not_found(self, client):
        response = client.patch("/api/v1/playlists/999/", json={"title": "Updated"})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_playlist(self, client, make_playlist):
        playlist = make_playlist()

        response = client.delete(f"/api/v1/playlists/{playlist.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT

        get_response = client.get(f"/api/v1/playlists/{playlist.id}/")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_playlist_not_found(self, client):
        response = client.delete("/api/v1/playlists/999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
