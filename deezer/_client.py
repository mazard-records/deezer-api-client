from typing import Any, Generic, TypeVar

from httpx import Client

from ._models import DeezerPlaylist


# TODO: bound to base type.
ModelClass = TypeVar("ModelClass")


class BaseProxy(Generic[ModelClass]):
    """ Base proxy class for client extension object. """

    def __init__(self, transport: Client, model: ModelClass) -> None:
        self._model = model
        self._transport = transport

    def __getattr__(self, attr: str) -> Any:
        # TODO: check if exist first.
        return getattr(self._model, attr)


class DeezerPlaylistProxy(BaseProxy[DeezerPlaylist]):
    """ """

    def add(self, track_ids: list[int]) -> None:
        songs = ",".join(track_ids)
        endpoint = self._url(f"/playlist/{self._model.id}/tracks")
        endpoint = f"{endpoint}&songs={songs}"
        response = self._transport.post(endpoint)
        response.raise_for_status()

    def remove(self, track_ids: list[int]) -> None:
        songs = ",".join(track_ids)
        endpoint = self._url(f"/playlist/{self._model.id}/tracks")
        endpoint = f"{endpoint}&songs={songs}"
        response = self._transport.delete(endpoint)
        response.raise_for_status()
   

class DeezerClient(object):

    def playlist(self, playlist_id: int) -> DeezerPlaylistProxy:
        raise NotImplementedError()

    def search(self, query: str) -> ...:
        raise NotImplementedError()
