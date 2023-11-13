from pydantic import AnyHttpUrl, BaseModel


class DeezerArtist(BaseModel):
    name: str


class DeezerAlbum(BaseModel):
    cover: AnyHttpUrl
    title: str


class DeezerTrack(BaseModel):
    artist: DeezerArtist
    album: DeezerAlbum
    id: int
    link: str
    preview: AnyHttpUrl
    title: str


class DeezerPlaylistTracks(BaseModel):
    data: list[DeezerTrack]


class DeezerPlaylist(BaseModel):
    tracks: DeezerPlaylistTracks
