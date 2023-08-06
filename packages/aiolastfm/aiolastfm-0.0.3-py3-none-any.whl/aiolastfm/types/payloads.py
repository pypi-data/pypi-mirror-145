# Future
from __future__ import annotations

# Standard Library
from typing import Literal, Optional, TypedDict

# Packages
from typing_extensions import NotRequired


##########
# Common #
##########

ImageData = TypedDict(
    "ImageData",
    {
        "size":  str,
        "#text": str
    }
)

TagData = TypedDict(
    "TagData",
    {
        "url":  str,
        "name": str
    }
)

WikiData = TypedDict(
    "WikiData",
    {
        "published": str,
        "summary":   str,
        "content":   str,
    }
)

TrackStreamableData = TypedDict(
    "TrackStreamableData",
    {
        "fulltrack": str,
        "#text":     str
    }
)

TrackArtistData = TypedDict(
    "TrackArtistData",
    {
        "url":  str,
        "name": str,
        "mbid": str
    }
)

#########
# Album #
#########

AlbumTrackPayload = TypedDict(
    "AlbumTrackPayload",
    {
        "streamable": TrackStreamableData,
        "duration":   Optional[int],
        "url":        str,
        "name":       str,
        "@attr":      dict[Literal["rank"], int],
        "artist":     TrackArtistData
    }
)

AlbumInfoPayload = TypedDict(
    "AlbumInfoPayload",
    {
        "artist":        str,
        "mbid":          str,
        "tags":          dict[Literal["tag"], list[TagData]],
        "playcount":     str,
        "image":         list[ImageData],
        "tracks":        dict[Literal["track"], list[AlbumTrackPayload]],
        "url":           str,
        "name":          str,
        "listeners":     str,
        "wiki":          WikiData,
        "userplaycount": NotRequired[int],
        # Same warnings on TrackPayload apply here.
    }
)

##########
# ARTIST #
##########

ArtistStatsData = TypedDict(
    "ArtistStatsData",
    {
        "listeners":     str,
        "playcount":     str,
        "userplaycount": NotRequired[str]
    }
)

SimilarArtistData = TypedDict(
    "SimilarArtistData",
    {
        "name":  str,
        "url":   str,
        "image": list[ImageData]
    }
)

ArtistBioLinkData = TypedDict(
    "ArtistBioLinkData",
    {
        "#text": str,
        "rel":   str,
        "href":  str,
    }
)

ArtistBioData = TypedDict(
    "ArtistBioData",
    {
        "links":     dict[Literal["link"], ArtistBioLinkData],
        "published": str,
        "summary":   str,
        "content":   str,
    }
)

ArtistInfoPayload = TypedDict(
    "ArtistInfoPayload",
    {
        "name":       str,
        "mbid":       str,
        "url":        str,
        "image":      list[ImageData],
        "streamable": str,
        "ontour":     str,
        "stats":      ArtistStatsData,
        "similar":    dict[Literal["artist"], list[SimilarArtistData]],
        "tags":       dict[Literal["tag"], list[TagData]],
        "bio":        ArtistBioData,
    }
)

#######
# TAG #
#######

TagWikiData = TypedDict(
    "TagWikiData",
    {
        "summary": str,
        "content": str
    }
)

TagInfoPayload = TypedDict(
    "TagInfoPayload",
    {
        "name":  str,
        "total": int,
        "reach": int,
        "wiki":  TagWikiData
    }
)

#########
# TRACK #
#########

TrackAlbumData = TypedDict(
    "TrackAlbumData",
    {
        "artist": str,
        "title":  str,
        "url":    str,
        "image":  list[ImageData]
    }
)

TrackInfoPayload = TypedDict(
    "TrackInfoPayload",
    {
        "name":          str,
        "url":           str,
        "duration":      str,
        "streamable":    TrackStreamableData,
        "listeners":     str,
        "playcount":     str,
        "artist":        TrackArtistData,
        "album":         TrackAlbumData,
        "toptags":       dict[Literal["tag"], TagData],
        "wiki":          WikiData,
        "userplaycount": NotRequired[str],
        "userloved":     NotRequired[str]
        # This payload can apparently contain "corrected" artist
        # and name fields however I couldn't get these to be
        # returned in my testing.
    }
)

########
# User #
########

UserRegisteredData = TypedDict(
    "UserRegisteredData",
    {
        "unixtime": str,
        "#text":    int
    }
)

UserInfoPayload = TypedDict(
    "UserInfoPayload",
    {
        "country":    str,
        "age":        str,
        "playcount":  str,
        "subscriber": str,
        "realname":   str,
        "playlists":  str,
        "bootstrap":  str,
        "image":      list[ImageData],
        "registered": UserRegisteredData,
        "url":        str,
        "gender":     str,
        "name":       str,
        "type":       str,
    }
)
