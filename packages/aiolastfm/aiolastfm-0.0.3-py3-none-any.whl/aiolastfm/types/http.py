# Future
from __future__ import annotations

# Standard Library
from typing import Literal


HTTPMethod = Literal[
    "GET",
    "POST"
]
APIMethod = Literal[
    # "album.addTags",
    "album.getInfo",
    "album.getTags",
    "album.getTopTags",
    # "album.removeTag",
    "album.search",

    # "artist.addTags",
    "artist.getCorrection",
    "artist.getInfo",
    "artist.getSimilar",
    "artist.getTags",
    "artist.getTopAlbums",
    "artist.getTopTags",
    "artist.getTopTracks",
    # "artist.removeTag",
    "artist.search",

    # "auth.getMobileSession",
    # "auth.getSession",
    # "auth.getToken",

    "chart.getTopArtists",
    "chart.getTopTags",
    "chart.getTopTracks",

    "geo.getTopArtists",
    "geo.getTopTracks",

    "library.getArtists",

    "tag.getInfo",
    "tag.getSimilar",
    "tag.getTopAlbums",
    "tag.getTopArtists",
    "tag.getTopTags",
    "tag.getTopTracks",
    "tag.getWeeklyArtistChart",

    # "track.addTags",
    "track.getCorrection",
    "track.getInfo",
    "track.getSimilar",
    "track.getTags",
    "track.getTopTags",
    # "track.love",
    # "track.removeTag",
    # "track.scrobble",
    "track.search",
    # "track.unlove",
    # "track.updateNowPlaying",

    "user.getFriends",
    "user.getInfo",
    "user.getLovedTracks",
    "user.getPersonalTags",
    "user.getRecentTracks",
    "user.getTopAlbums",
    "user.getTopArtists",
    "user.getTopTags",
    "user.getTopTracks",
    "user.getWeeklyAlbumChart",
    "user.getWeeklyArtistChart",
    "user.getWeeklyChartList",
    "user.getWeeklyTrackChart",
]
