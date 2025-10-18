from starlette import status

from src.tests.conftest import sample_image_base64


class TestPlaylistsAPI:

    def test_create_playlist(self, client, sample_image_base64, mock_s3_client_put):
        sample_playlist_data = {
            "title": "Test Playlist",
            "description": "A test playlist for unit testing",
            "cover_image": sample_image_base64,
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

        # upload pic s3
        mock_s3_client_put.assert_called_once()

    def test_create_empty_playlist(self, client):
        minimal_data = {}
        response = client.post("/api/v1/playlists/", json=minimal_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "New Playlist #1"
        assert data["cover_url"] is None

    def test_get_playlists(self, client, make_playlist):
        make_playlist()

        response = client.get("/api/v1/playlists/")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1

    def test_get_playlists_ordering(self, client, make_playlist):
        """Favorites first, then by created_at"""
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

    def test_update_playlist_mark_as_favorite_success(self, client, make_playlist):
        playlist = make_playlist()

        response = client.patch(
            f"/api/v1/playlists/{playlist.id}/", json={"is_favorite": True}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_favorite"] == playlist.is_favorite == True

    def test_update_playlist_upload_new_cover_success(
        self, client, make_playlist, sample_image_base64, mock_s3_client_put
    ):
        playlist = make_playlist()

        response = client.patch(
            f"/api/v1/playlists/{playlist.id}/",
            json={"cover_image": sample_image_base64},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["cover_url"] is not None
        assert data["cover_url"].startswith("https://")
        assert "covers/" in data["cover_url"]

        mock_s3_client_put.assert_called_once()

    def test_update_with_same_image_generates_unique_cover_key(
        self, make_playlist, sample_image_base64, mock_s3_client_put, client
    ):
        playlist = make_playlist()
        first_response = client.patch(
            f"/api/v1/playlists/{playlist.id}/",
            json={"cover_image": sample_image_base64},
        )
        first_cover_url = first_response

        second_response = client.patch(
            f"/api/v1/playlists/{playlist.id}/",
            json={"cover_image": sample_image_base64},
        )
        second_cover_url = second_response

        assert second_cover_url != first_cover_url

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
