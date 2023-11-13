


class DeezerPlaylistProxy(...):

    def add(self, track_ids: list[int]) -> None:
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.post(endpoint)
        response.raise_for_status()

    def remove(self, track_ids: list[int]) -> None:
        endpoint = self._url(f"/playlist/{playlist.id}/tracks")
        endpoint = f"{endpoint}&songs={track.id}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()
   

class DeezerClient(object):

    def playlist(self, playlist_id: int) -> ...:
        raise NotImplementedError()

    def search(self, query: str) -> ...:
        raise NotImplementedError()
