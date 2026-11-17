"""Validate fixture and compute a CSV-only oracle independent of Cypher."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURE = ROOT / "fixture"


def read_fixture(directory=FIXTURE):
    manifest = json.loads((directory / "manifest.json").read_text())
    for name, digest in manifest["sha256"].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest() != digest:
            raise ValueError(f"Fixture hash mismatch: {name}")
    tracks = list(csv.DictReader((directory/"tracks.csv").open()))
    playlists = list(csv.DictReader((directory/"playlists.csv").open()))
    if {"tracks.csv": len(tracks), "playlists.csv": len(playlists)} != manifest["csv_rows"]:
        raise ValueError("Fixture row count mismatch")
    track_ids = {r["track_id"] for r in tracks}
    if any(r["track_id"] not in track_ids for r in playlists):
        raise ValueError("Playlist references missing metadata")
    for row in playlists:
        row["position"] = int(row["position"])
        if row["position"] < 1:
            raise ValueError("Position must be positive")
    # Check display values are consistent for identifiers, including collaborations.
    for rows, keys in [(tracks, [("track_id","track_name"),("artist_id","artist_name"),("album_id","album_name")]),
                       (playlists, [("playlist_id","playlist_name"),("playlist_id","user_id")])]:
        for key, value in keys:
            values = {}
            for row in rows:
                if row[key] in values and values[row[key]] != row[value]:
                    raise ValueError(f"Conflicting {value} for {row[key]}")
                values[row[key]] = row[value]
    return manifest, tracks, playlists


def expected_answers(tracks, playlists, source="P01"):
    artist_names = {r['artist_id']:r['artist_name'] for r in tracks}
    credits = {}
    for row in tracks:
        credits.setdefault(row['track_id'],set()).add(row['artist_id'])
    playlist_tracks = {}
    playlist_names = {}
    for row in playlists:
        playlist_tracks.setdefault(row['playlist_id'],set()).add(row['track_id'])
        playlist_names[row['playlist_id']] = row['playlist_name']
    if source not in playlist_tracks:
        raise ValueError("Unknown source playlist")
    appearances = {a:set() for a in artist_names}
    for p, tids in playlist_tracks.items():
        for tid in tids:
            for artist in credits[tid]:
                appearances[artist].add(p)
    a = [{"artist_id":artist,"artist_name":artist_names[artist],"playlist_count":len(ps)}
         for artist, ps in appearances.items() if ps]
    a.sort(key=lambda row:(-row['playlist_count'],row['artist_id']))
    b = []
    for pid, tids in playlist_tracks.items():
        overlap = tids & playlist_tracks[source]
        if pid != source and overlap:
            b.append({"playlist_id":pid,"playlist_name":playlist_names[pid],"shared_tracks":len(overlap)})
    b.sort(key=lambda row:(-row['shared_tracks'],row['playlist_id']))
    return {"question_a":a[:5],"question_b":b[:5]}


def graph_counts(tracks, playlists):
    return {**{label:len({r[key] for r in rows}) for label,key,rows in [
        ('Track','track_id',tracks),('Artist','artist_id',tracks),('Album','album_id',tracks),
        ('Playlist','playlist_id',playlists),('User','user_id',playlists)]},
        "OWNS":len({(r['user_id'],r['playlist_id']) for r in playlists}),
        "PLAYLIST_HAS_TRACK":len({(r['playlist_id'],r['track_id'],r['position']) for r in playlists}),
        "ALBUM_HAS_TRACK":len({(r['album_id'],r['track_id']) for r in tracks}),
        "ARTIST":len({(r['track_id'],r['artist_id']) for r in tracks})}


if __name__ == "__main__":
    manifest, tracks, playlists = read_fixture()
    assert graph_counts(tracks,playlists) == manifest['expected_graph']
    print(json.dumps({"fixture":manifest['version'],**expected_answers(tracks,playlists)},indent=2))
