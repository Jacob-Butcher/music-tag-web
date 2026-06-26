import collections

from django.db.models import Count, functions, Sum
from rest_framework import serializers

from applications.music.models import Track
from applications.subsonic.utils import get_type_from_ext


def to_subsonic_date(date):
    """
    Subsonic expects this kind of date format: 2012-04-17T19:55:49.000Z
    """

    if not date:
        return

    return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def get_valid_filepart(s):
    """
    Return a string suitable for use in a file path. Escape most non-ASCII
    chars, and truncate the string to a suitable length too.
    """
    max_length = 50
    keepcharacters = " ._()[]-+"
    final = "".join(
        c if c.isalnum() or c in keepcharacters else "_" for c in s
    ).rstrip()
    return final[:max_length]


def get_track_path(track, suffix):
    parts = []
    parts.append(get_valid_filepart(track.artist.name))
    if track.album:
        parts.append(get_valid_filepart(track.album.name))
    track_part = get_valid_filepart(track.name) + "." + suffix
    if track.track_number:
        track_part = f"{track.track_number} - {track_part}"
    parts.append(track_part)
    return "/".join(parts)


def get_artist_data(artist_values):
    return {
        "id": artist_values["id"],
        "name": artist_values["name"],
        "albumCount": artist_values["_albums_count"],
        "coverArt": "ar-{}".format(artist_values["id"]),
    }


class GetArtistsSerializer(serializers.Serializer):
    def to_representation(self, queryset):
        payload = {"ignoredArticles": "", "index": []}
        queryset = queryset.order_by(functions.Lower("name"))
        queryset = queryset.annotate(_albums_count=Count("albums"))
        values = queryset.values("id", "_albums_count", "name")

        first_letter_mapping = collections.defaultdict(list)
        for artist in values:
            if artist["name"]:
                first_letter_mapping[artist["name"][0].upper()].append(artist)

        for letter, artists in sorted(first_letter_mapping.items()):
            letter_data = {
                "name": letter,
                "artist": [get_artist_data(v) for v in artists],
            }
            payload["index"].append(letter_data)
        return payload


class GetArtistSerializer(serializers.Serializer):
    def to_representation(self, artist):
        albums = artist.albums.annotate(
            _song_count=Count("tracks"),
            _duration=Sum("tracks__duration")
        )
        payload = {
            "id": artist.pk,
            "name": artist.name,
            "albumCount": albums.count(),
            "album": [],
        }
        if artist.attachment_cover_id:
            payload["coverArt"] = f"ar-{artist.id}"
        for album in albums:
            album_data = {
                "id": album.id,
                "artistId": artist.id,
                "name": album.name,
                "artist": artist.name,
                "created": to_subsonic_date(album.created_at),
                "songCount": album._song_count,
                "duration": album._duration or 0
            }
            if album.attachment_cover_id:
                album_data["coverArt"] = f"al-{album.id}"
            if album.max_year:
                album_data["year"] = album.max_year
            payload["album"].append(album_data)
        return payload


def get_track_data(track):
    """
    subsonic expects this kind of data:
    """
    album = track.album
    artist = track.artist
    data = {
        "id": track.pk,
        "isDir": "false",
        "title": track.name,
        "album": album.name if album else "",
        "artist": artist.name,
        "track": track.track_number or 1,
        "discNumber": track.disc_number or 1,
        "contentType": track.mimetype or get_type_from_ext(track.path),
        "suffix": track.suffix or "",
        "path": get_track_path(track, track.suffix or "mp3"),
        "duration": track.duration or 0,
        "created": to_subsonic_date(track.created_at),
        "albumId": album.pk if album else "",
        "artistId": album.artist.pk if album else track.artist.pk,
        "type": "music",
    }
    if album and album.attachment_cover_id:
        data["coverArt"] = f"al-{album.id}"
    if track.bit_rate:
        data["bitrate"] = int(track.bit_rate / 1000)
    if track.size:
        data["size"] = track.size
    if album and album.max_year:
        data["year"] = album.max_year
    else:
        data["year"] = track.created_at.year
    return data


def get_album2_data(album, annotated=False):
    """
    subsonic expects this kind of data:
    If annotated=True, the album queryset must have _song_count and _duration annotations.
    """
    payload = {
        "id": album.id,
        "artistId": album.artist_id,
        "name": album.name,
        "artist": album.artist.name,
        "created": to_subsonic_date(album.created_at),
        "duration": album._duration if annotated else album.tracks.aggregate(duration_count=Sum("duration")).get("duration_count", 0),
        "playCount": 1,
    }
    if album.attachment_cover_id:
        payload["coverArt"] = f"al-{album.id}"
    if album.genre:
        payload["genre"] = album.genre.name
    if album.max_year:
        payload["year"] = album.max_year
    payload["songCount"] = album._song_count if annotated else album.tracks.count()
    return payload


def get_song_list_data(tracks):
    return [get_track_data(track) for track in tracks]


class GetAlbumSerializer(serializers.Serializer):
    def to_representation(self, album):
        payload = get_album2_data(album)

        tracks = album.tracks.all()
        payload["song"] = get_song_list_data(tracks)
        return payload


class GetSongSerializer(serializers.Serializer):
    def to_representation(self, track):
        return get_track_data(track)


def get_starred_tracks_data(favorites):
    by_track_id = {f.track_id: f for f in favorites}
    tracks = (
        Track.objects.filter(pk__in=by_track_id.keys())
            .select_related("album__artist")
    )
    tracks = tracks.order_by("-created_at")
    data = []
    for t in tracks:
        td = get_track_data(t)
        td["starred"] = to_subsonic_date(by_track_id[t.pk].created_at)
        data.append(td)
    return data


def get_album_list2_data(albums):
    albums = albums.annotate(
        _song_count=Count("tracks"),
        _duration=Sum("tracks__duration")
    )
    return [get_album2_data(a, annotated=True) for a in albums]


def get_playlist_data(playlist):
    return {
        "id": playlist.pk,
        "name": playlist.name,
        "owner": playlist.user.username,
        "public": "false",
        "songCount": 0,
        "duration": 0,
        "created": to_subsonic_date(playlist.creation_date),
    }
