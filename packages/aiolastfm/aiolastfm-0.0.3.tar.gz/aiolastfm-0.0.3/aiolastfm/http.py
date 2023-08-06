# Future
from __future__ import annotations

# Standard Library
import asyncio
import logging
from typing import Any, Literal

# Packages
import aiohttp

# Local
from .exceptions import EXCEPTION_MAPPING, HTTPException, InvalidResponse
from .types.http import APIMethod, HTTPMethod
from .types.payloads import AlbumInfoPayload, ArtistInfoPayload, TagInfoPayload, TrackInfoPayload, UserInfoPayload
from .utilities import MISSING, json_or_text


__all__ = (
    "HTTPClient",
)

__log__: logging.Logger = logging.getLogger("aiolastfm.http")


class HTTPClient:
    """
    Client used to make HTTP requests to the Last.fm API.

    Parameters
    -----------
    client_key
        The API key to use for requests.
    client_secret
        The API secret to use for requests.
    session
        The session to use for requests.
    """

    _BASE_URL: str = "https://ws.audioscrobbler.com/2.0/"
    _USER_AGENT: str = f"aiolastfm/0.0.3 (https://github.com/Axelware/aiolastfm)"
    _HEADERS: dict[str, str] = {
        "User-Agent": _USER_AGENT,
    }

    def __init__(
        self,
        *,
        client_key: str,
        client_secret: str | None = None,
        session: aiohttp.ClientSession | None = None,
    ) -> None:

        self._client_key: str = client_key
        self._client_secret: str | None = client_secret
        self._session: aiohttp.ClientSession | None = session

    def __repr__(self) -> str:
        return "<aiolastfm.HTTPClient>"

    ###########
    # Private #
    ###########

    async def _get_session(self) -> aiohttp.ClientSession:

        if not self._session:
            self._session = aiohttp.ClientSession()

        return self._session

    async def _request(
        self,
        _method: HTTPMethod, /,
        *,
        method: APIMethod,
        **parameters: Any
    ) -> Any:

        session = await self._get_session()

        params: dict[str, Any] = {
            "format":  "json",
            "api_key": self._client_key,
            "method":  method,
        }
        params |= {k: v for k, v in parameters.items() if v is not None}

        response: aiohttp.ClientResponse = MISSING
        data: dict[str, Any] | str = MISSING

        for tries in range(3):

            try:

                async with session.request(
                        _method, url=self._BASE_URL,
                        params=params,
                        headers=self._HEADERS
                ) as response:

                    data = await json_or_text(response)

                    if isinstance(data, str):
                        raise InvalidResponse

                    if code := data.get("error"):
                        raise EXCEPTION_MAPPING[code](response, data)

                    if 200 <= response.status < 300:
                        return data

                    await asyncio.sleep(1 + tries * 2)
                    continue

            except OSError as error:
                if tries < 2 and error.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        assert not isinstance(data, str)
        raise HTTPException(response, data=data)

    ##########
    # Public #
    ##########

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    # Albums

    async def add_album_tags(self) -> None:
        raise NotImplementedError

    async def get_album_info(
        self,
        *,
        name: str | None = None,
        artist: str | None = None,
        musicbrainz_id: str | None = None,
        auto_correct: bool | None = None,
        username: str | None = None,
        language_code: str | None = None,
    ) -> AlbumInfoPayload:

        data: dict[Literal["album"], AlbumInfoPayload] = await self._request(
            "GET",
            method="album.getInfo",
            album=name,
            artist=artist,
            mbid=musicbrainz_id,
            autocorrect=int(auto_correct) if auto_correct else None,
            username=username,
            lang=language_code
        )
        return data["album"]

    async def get_albums_tags(self) -> None:
        raise NotImplementedError

    async def get_albums_top_tags(self) -> None:
        raise NotImplementedError

    async def remove_album_tag(self) -> None:
        raise NotImplementedError

    async def search_for_albums(self) -> None:
        raise NotImplementedError

    # Artists

    async def add_artist_tags(self) -> None:
        raise NotImplementedError

    async def get_artist_correction(self) -> None:
        raise NotImplementedError

    async def get_artist_info(
        self,
        *,
        name: str | None = None,
        musicbrainz_id: str | None = None,
        auto_correct: bool | None = None,
        username: str | None = None,
        language_code: str | None = None,
    ) -> ArtistInfoPayload:

        data: dict[Literal["artist"], ArtistInfoPayload] = await self._request(
            "GET",
            method="artist.getInfo",
            artist=name,
            mbid=musicbrainz_id,
            autocorrect=int(auto_correct) if auto_correct else None,
            username=username,
            lang=language_code
        )
        return data["artist"]

    async def get_similar_artists(self) -> None:
        raise NotImplementedError

    async def get_artists_tags(self) -> None:
        raise NotImplementedError

    async def get_artists_top_albums(self) -> None:
        raise NotImplementedError

    async def get_artists_top_tags(self) -> None:
        raise NotImplementedError

    async def remove_artist_tag(self) -> None:
        raise NotImplementedError

    async def search_for_artists(self) -> None:
        raise NotImplementedError

    # Auth

    async def get_mobile_auth_session(self) -> None:
        raise NotImplementedError

    async def get_auth_session(self) -> None:
        raise NotImplementedError

    async def get_auth_token(self) -> None:
        raise NotImplementedError

    # Chart

    async def get_charts_top_artists(self) -> None:
        raise NotImplementedError

    async def get_charts_top_tags(self) -> None:
        raise NotImplementedError

    async def get_charts_top_tracks(self) -> None:
        raise NotImplementedError

    # Geo

    async def get_geo_top_artists(self) -> None:
        raise NotImplementedError

    async def get_geo_top_tracks(self) -> None:
        raise NotImplementedError

    # Library

    async def get_library_artists(self) -> None:
        raise NotImplementedError

    # Tag

    async def get_tag_info(
        self,
        tag: str, /,
        *,
        language_code: str | None = None
    ) -> TagInfoPayload:

        data: dict[Literal["tag"], TagInfoPayload] = await self._request(
            "GET",
            method="tag.getInfo",
            tag=tag,
            lang=language_code
        )
        return data["tag"]

    async def get_similar_tags(self) -> None:
        raise NotImplementedError

    async def get_tags_top_albums(self) -> None:
        raise NotImplementedError

    async def get_tags_top_artists(self) -> None:
        raise NotImplementedError

    async def get_tags_top_tags(self) -> None:
        raise NotImplementedError

    async def get_tags_top_tracks(self) -> None:
        raise NotImplementedError

    async def get_tags_weekly_artist_chart(self) -> None:
        raise NotImplementedError

    # Track

    async def add_track_tags(self) -> None:
        raise NotImplementedError

    async def get_track_correction(self) -> None:
        raise NotImplementedError

    async def get_track_info(
        self,
        *,
        name: str | None = None,
        artist: str | None = None,
        musicbrainz_id: str | None = None,
        auto_correct: bool | None = None,
        username: str | None = None,
    ) -> TrackInfoPayload:

        data: dict[Literal["track"], TrackInfoPayload] = await self._request(
            "GET",
            method="track.getInfo",
            track=name,
            artist=artist,
            mbid=musicbrainz_id,
            autocorrect=int(auto_correct) if auto_correct else None,
            username=username,
        )
        return data["track"]

    async def get_similar_tracks(self) -> None:
        raise NotImplementedError

    async def get_tracks_tags(self) -> None:
        raise NotImplementedError

    async def get_tracks_top_tags(self) -> None:
        raise NotImplementedError

    async def love_track(self) -> None:
        raise NotImplementedError

    async def remove_track_tag(self) -> None:
        raise NotImplementedError

    async def scrobble_track(self) -> None:
        raise NotImplementedError

    async def search_for_tracks(self) -> None:
        raise NotImplementedError

    async def unlove_track(self) -> None:
        raise NotImplementedError

    async def update_currently_playing_track(self) -> None:
        raise NotImplementedError

    # User

    async def get_users_friends(self) -> None:
        raise NotImplementedError

    async def get_user_info(
        self,
        user: str, /
    ) -> UserInfoPayload:

        # This method could have 'user' be optional as the
        # api defaults to the authenticated user but as of
        # implementation this library does not support user
        # authentication.
        data: dict[Literal["user"], UserInfoPayload] = await self._request(
            "GET",
            method="user.getInfo",
            user=user
        )
        return data["user"]

    async def get_users_loved_tracks(self) -> None:
        raise NotImplementedError

    async def get_users_personal_tags(self) -> None:
        raise NotImplementedError

    async def get_users_recent_tracks(self) -> None:
        raise NotImplementedError

    async def get_users_top_albums(self) -> None:
        raise NotImplementedError

    async def get_users_top_artists(self) -> None:
        raise NotImplementedError

    async def get_users_top_tags(self) -> None:
        raise NotImplementedError

    async def get_users_top_tracks(self) -> None:
        raise NotImplementedError

    async def get_users_weekly_album_chart(self) -> None:
        raise NotImplementedError

    async def get_users_weekly_artist_chart(self) -> None:
        raise NotImplementedError

    async def get_users_weekly_chart_list(self) -> None:
        raise NotImplementedError

    async def get_users_weekly_track_chart(self) -> None:
        raise NotImplementedError
