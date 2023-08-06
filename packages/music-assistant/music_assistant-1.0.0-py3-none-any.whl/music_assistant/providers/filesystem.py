"""Filesystem musicprovider support for MusicAssistant."""
import base64
import os
import re
from typing import List, Optional
import aiofiles

import taglib

from music_assistant.models.errors import InvalidDataError
from music_assistant.helpers.util import parse_title_and_version
from music_assistant.models.media_items import (
    Album,
    Artist,
    ContentType,
    MediaItemProviderId,
    MediaItemType,
    MediaQuality,
    MediaType,
    Playlist,
    StreamDetails,
    StreamType,
    Track,
)
from music_assistant.models.provider import MusicProvider


class FileSystemProvider(MusicProvider):
    """
    Very basic implementation of a musicprovider for local files.

    Assumes files are stored on disk in format <artist>/<album>/<track.ext>
    Reads ID3 tags from file and falls back to parsing filename
    Supports m3u files only for playlists
    Supports having URI's from streaming providers within m3u playlist
    Should be compatible with LMS
    """

    # pylint chokes on taglib so ignore these
    # pylint: disable=unsubscriptable-object,unsupported-membership-test

    def __init__(self, music_dir: str, playlist_dir: str | None = None) -> None:
        """
        Initialize the Filesystem provider.

        music_dir: Directory on disk containing music files
        playlist_dir: Directory on disk containing playlist files (optional)

        """
        self._attr_id = "filesystem"
        self._attr_name = "Filesystem"
        self._playlists_dir = playlist_dir
        self._music_dir = music_dir
        self._attr_supported_mediatypes = [
            MediaType.ARTIST,
            MediaType.ALBUM,
            MediaType.TRACK,
        ]
        if playlist_dir is not None:
            self._attr_supported_mediatypes.append(MediaType.PLAYLIST)

    async def setup(self) -> None:
        """Handle async initialization of the provider."""
        if not os.path.isdir(self._music_dir):
            raise FileNotFoundError(f"Music Directory {self._music_dir} does not exist")
        if self._playlists_dir is not None and not os.path.isdir(self._playlists_dir):
            raise FileNotFoundError(
                f"Playlist Directory {self._playlists_dir} does not exist"
            )

    async def search(
        self, search_query: str, media_types=Optional[List[MediaType]], limit: int = 5
    ) -> List[MediaItemType]:
        """
        Perform search on musicprovider.

            :param search_query: Search query.
            :param media_types: A list of media_types to include. All types if None.
            :param limit: Number of items to return in the search (per type).
        """
        # TODO !
        return []

    async def get_library_artists(self) -> List[Artist]:
        """Retrieve all library artists."""
        if not os.path.isdir(self._music_dir):
            self.logger.error("music path does not exist: %s", self._music_dir)
            return None
        result = []
        for dirname in os.listdir(self._music_dir):
            dirpath = os.path.join(self._music_dir, dirname)
            if os.path.isdir(dirpath) and not dirpath.startswith("."):
                artist = await self.get_artist(dirpath)
                if artist:
                    result.append(artist)
        return result

    async def get_library_albums(self) -> List[Album]:
        """Get album folders recursively."""
        result = []
        for artist in await self.get_library_artists():
            for album in await self.get_artist_albums(artist.item_id):
                result.append(album)
        return result

    async def get_library_tracks(self) -> List[Track]:
        """Get all tracks recursively."""
        # TODO: support disk subfolders
        result = []
        for album in await self.get_library_albums():
            for track in await self.get_album_tracks(album.item_id):
                result.append(track)
        return result

    async def get_library_playlists(self) -> List[Playlist]:
        """Retrieve playlists from disk."""
        if not self._playlists_dir:
            return []
        result = []
        for filename in os.listdir(self._playlists_dir):
            filepath = os.path.join(self._playlists_dir, filename)
            if (
                os.path.isfile(filepath)
                and not filename.startswith(".")
                and filename.lower().endswith(".m3u")
            ):
                playlist = await self.get_playlist(filepath)
                if playlist:
                    result.append(playlist)
        return result

    async def get_artist(self, prov_artist_id: str) -> Artist:
        """Get full artist details by id."""
        if os.sep not in prov_artist_id:
            itempath = base64.b64decode(prov_artist_id).decode("utf-8")
        else:
            itempath = prov_artist_id
            prov_artist_id = base64.b64encode(itempath.encode("utf-8")).decode("utf-8")
        if not os.path.isdir(itempath):
            self.logger.error("Artist path does not exist: %s", itempath)
            return None
        name = itempath.split(os.sep)[-1]
        artist = Artist(item_id=prov_artist_id, provider=self.id, name=name)
        artist.provider_ids.append(
            MediaItemProviderId(provider=self.id, item_id=artist.item_id)
        )
        return artist

    async def get_album(self, prov_album_id: str) -> Album:
        """Get full album details by id."""
        if os.sep not in prov_album_id:
            itempath = base64.b64decode(prov_album_id).decode("utf-8")
        else:
            itempath = prov_album_id
            prov_album_id = base64.b64encode(itempath.encode("utf-8")).decode("utf-8")
        if not os.path.isdir(itempath):
            self.logger.error("album path does not exist: %s", itempath)
            return None
        name = itempath.split(os.sep)[-1]
        artistpath = itempath.rsplit(os.sep, 1)[0]
        name, version = parse_title_and_version(name)
        album = Album(
            item_id=prov_album_id, provider=self.id, name=name, version=version
        )
        album.artist = await self.get_artist(artistpath)
        if not album.artist:
            raise InvalidDataError(f"No album artist ! {artistpath}")
        album.provider_ids.append(
            MediaItemProviderId(provider=self.id, item_id=prov_album_id)
        )
        return album

    async def get_track(self, prov_track_id: str) -> Track:
        """Get full track details by id."""
        if os.sep not in prov_track_id:
            itempath = base64.b64decode(prov_track_id).decode("utf-8")
        else:
            itempath = prov_track_id
        if not os.path.isfile(itempath):
            self.logger.error("track path does not exist: %s", itempath)
            return None
        return await self._parse_track(itempath)

    async def get_playlist(self, prov_playlist_id: str) -> Playlist:
        """Get full playlist details by id."""
        if os.sep not in prov_playlist_id:
            itempath = base64.b64decode(prov_playlist_id).decode("utf-8")
        else:
            itempath = prov_playlist_id
            prov_playlist_id = base64.b64encode(itempath.encode("utf-8")).decode(
                "utf-8"
            )
        if not os.path.isfile(itempath):
            self.logger.error("playlist path does not exist: %s", itempath)
            return None
        name = itempath.split(os.sep)[-1].replace(".m3u", "")
        playlist = Playlist(prov_playlist_id, provider=self.id, name=name)
        playlist.is_editable = True
        playlist.provider_ids.append(
            MediaItemProviderId(provider=self.id, item_id=prov_playlist_id)
        )
        playlist.owner = "disk"
        playlist.checksum = os.path.getmtime(itempath)
        return playlist

    async def get_album_tracks(self, prov_album_id) -> List[Track]:
        """Get album tracks for given album id."""
        result = []
        if os.sep not in prov_album_id:
            albumpath = base64.b64decode(prov_album_id).decode("utf-8")
        else:
            albumpath = prov_album_id
        if not os.path.isdir(albumpath):
            self.logger.error("album path does not exist: %s", albumpath)
            return []
        album = await self.get_album(albumpath)
        for filename in os.listdir(albumpath):
            filepath = os.path.join(albumpath, filename)
            if os.path.isfile(filepath) and not filepath.startswith("."):
                track = await self._parse_track(filepath)
                if track:
                    track.album = album
                    result.append(track)
        return result

    async def get_playlist_tracks(self, prov_playlist_id: str) -> List[Track]:
        """Get playlist tracks for given playlist id."""
        result = []
        if os.sep not in prov_playlist_id:
            itempath = base64.b64decode(prov_playlist_id).decode("utf-8")
        else:
            itempath = prov_playlist_id
        if not os.path.isfile(itempath):
            self.logger.error("playlist path does not exist: %s", itempath)
            return result
        index = 0
        async with aiofiles.open(itempath, "r") as _file:
            for line in await _file.readlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    track = await self._parse_track_from_uri(line)
                    if track:
                        result.append(track)
                        index += 1
        return result

    async def get_artist_albums(self, prov_artist_id: str) -> List[Album]:
        """Get a list of albums for the given artist."""
        result = []
        if os.sep not in prov_artist_id:
            artistpath = base64.b64decode(prov_artist_id).decode("utf-8")
        else:
            artistpath = prov_artist_id
        if not os.path.isdir(artistpath):
            self.logger.error("artist path does not exist: %s", artistpath)
            return
        for dirname in os.listdir(artistpath):
            dirpath = os.path.join(artistpath, dirname)
            if os.path.isdir(dirpath) and not dirpath.startswith("."):
                album = await self.get_album(dirpath)
                if album:
                    result.append(album)
        return result

    async def get_artist_toptracks(self, prov_artist_id: str) -> List[Track]:
        """Get a list of random tracks as we have no clue about preference."""
        result = []
        for album in await self.get_artist_albums(prov_artist_id):
            for track in await self.get_album_tracks(album.item_id):
                result.append(track)
        return result

    async def get_stream_details(self, item_id: str) -> StreamDetails:
        """Return the content details for the given track when it will be streamed."""
        if os.sep not in item_id:
            track_id = base64.b64decode(item_id).decode("utf-8")
        if not os.path.isfile(track_id):
            return None
        # TODO: retrieve sanple rate and bitdepth
        return StreamDetails(
            type=StreamType.FILE,
            provider=self.id,
            item_id=item_id,
            content_type=ContentType(track_id.split(".")[-1]),
            path=track_id,
            sample_rate=44100,
            bit_depth=16,
        )

    async def _parse_track(self, filename):
        """Try to parse a track from a filename with taglib."""
        # pylint: disable=broad-except
        try:
            song = taglib.File(filename)
        except Exception:
            return None  # not a media file ?
        prov_item_id = base64.b64encode(filename.encode("utf-8")).decode("utf-8")
        try:
            name = song.tags["TITLE"][0]
        except KeyError:
            name = filename.split("/")[-1].split(".")[0]
        name, version = parse_title_and_version(name)
        track = Track(
            item_id=prov_item_id, provider=self.id, name=name, version=version
        )
        track.duration = song.length
        albumpath = filename.rsplit(os.sep, 1)[0]
        track.album = await self.get_album(albumpath)
        if "ARTIST" in song.tags:
            artists = []
            for artist_str in song.tags["ARTIST"]:
                local_artist_path = os.path.join(self._music_dir, artist_str)
                if os.path.isfile(local_artist_path):
                    artist = await self.get_artist(local_artist_path)
                else:
                    fake_artistpath = os.path.join(self._music_dir, artist_str)
                    artist = Artist(
                        item_id=fake_artistpath, provider=self.id, name=artist_str
                    )
                    artist.provider_ids.append(
                        MediaItemProviderId(
                            provider=self.id,
                            item_id=base64.b64encode(
                                fake_artistpath.encode("utf-8")
                            ).decode("utf-8"),
                        )
                    )
                artists.append(artist)
            track.artists = artists
        else:
            artistpath = filename.rsplit(os.sep, 2)[0]
            artist = await self.get_artist(artistpath)
            track.artists.append(artist)
        if "GENRE" in song.tags:
            track.metadata["genres"] = song.tags["GENRE"]
        if "ISRC" in song.tags and song.tags["ISRC"]:
            track.isrc = song.tags["ISRC"][0]
        if "DISCNUMBER" in song.tags and song.tags["DISCNUMBER"]:
            regexp_numbers = re.findall(r"\d+", song.tags["DISCNUMBER"][0])
            track.disc_number = int(regexp_numbers[0] if regexp_numbers else "0")
        if "TRACKNUMBER" in song.tags and song.tags["TRACKNUMBER"]:
            regexp_numbers = re.findall(r"\d+", song.tags["TRACKNUMBER"][0])
            track.track_number = int(regexp_numbers[0] if regexp_numbers else "0")
        quality_details = ""
        if filename.endswith(".flac"):
            # TODO: get bit depth
            quality = MediaQuality.FLAC_LOSSLESS
            if song.sampleRate > 192000:
                quality = MediaQuality.FLAC_LOSSLESS_HI_RES_4
            elif song.sampleRate > 96000:
                quality = MediaQuality.FLAC_LOSSLESS_HI_RES_3
            elif song.sampleRate > 48000:
                quality = MediaQuality.FLAC_LOSSLESS_HI_RES_2
            quality_details = f"{song.sampleRate / 1000} Khz"
        elif filename.endswith(".ogg"):
            quality = MediaQuality.LOSSY_OGG
            quality_details = f"{song.bitrate} kbps"
        elif filename.endswith(".m4a"):
            quality = MediaQuality.LOSSY_AAC
            quality_details = f"{song.bitrate} kbps"
        else:
            quality = MediaQuality.LOSSY_MP3
            quality_details = f"{song.bitrate} kbps"
        track.provider_ids.append(
            MediaItemProviderId(
                provider=self.id,
                item_id=prov_item_id,
                quality=quality,
                details=quality_details,
            )
        )
        return track

    async def _parse_track_from_uri(self, uri):
        """Try to parse a track from an uri found in playlist."""
        # pylint: disable=broad-except
        if "://" in uri:
            # track is uri from external provider?
            try:
                return await self.mass.music.get_item_by_uri(uri)
            except Exception as exc:
                self.logger.warning(
                    "Could not parse uri %s to track: %s", uri, str(exc)
                )
                return None
        # try to treat uri as filename
        # TODO: filename could be related to musicdir or full path
        track = await self.get_track(uri)
        if track:
            return track
        track = await self.get_track(os.path.join(self._music_dir, uri))
        if track:
            return track
        return None
