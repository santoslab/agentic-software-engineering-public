"""Create original fictional music data, deterministically. No downloaded music data."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VERSION = "fictional-music-v1"
NAMES = ["Amber Circuit", "Blue Orchard", "Copper Kite", "Delta Lantern",
         "Echo Harbor", "Fern Signal", "Glass Meadow", "Indigo Current"]


def write(name, fields, rows):
    with (ROOT / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build():
    tracks = []
    for i in range(1, 37):
        credits = [(i - 1) // 6 + 1]
        if i in [1, 7, 13, 19, 25, 31]:
            credits.append(7)
        if i in [2, 8, 14, 20, 26, 32]:
            credits.append(8)
        for artist in credits:
            tracks.append(dict(track_id=f"T{i:02}", track_name=f"Signal {i:02}",
                               album_id=f"L{(i-1)//6+1:02}", album_name=f"Chapter {(i-1)//6+1}",
                               artist_id=f"A{artist:02}", artist_name=NAMES[artist-1]))
    selections = [list(range(1, 11)), list(range(1, 7))+list(range(11, 17)),
                  list(range(3, 9))+list(range(17, 23)), list(range(9, 15))+list(range(23, 29)),
                  list(range(15, 21))+list(range(29, 35)), list(range(21, 27))+[35,36,1,2],
                  list(range(27, 33))+[3,4,5,6], list(range(33, 37))+list(range(7, 13))]
    playlists = []
    for p, selection in enumerate(selections, 1):
        for position, track in enumerate(selection, 1):
            playlists.append(dict(playlist_id=f"P{p:02}", playlist_name="Evening" if p in [3,4] else f"Mix {p}",
                                  user_id=f"U{(p-1)//2+1:02}", track_id=f"T{track:02}", position=position))
    playlists.append(dict(playlists[0], position=11))  # intentional second occurrence
    playlists.extend(dict(playlists[i]) for i in [0, 12, 25])  # exact duplicates
    write("tracks.csv", list(tracks[0]), tracks)
    write("playlists.csv", list(playlists[0]), playlists)
    occurrences = {(r['playlist_id'], r['track_id'], r['position']) for r in playlists}
    counts = {"Track": 36, "Artist": 8, "Album": 6, "Playlist": 8, "User": 4,
              "OWNS": 8, "PLAYLIST_HAS_TRACK": len(occurrences), "ALBUM_HAS_TRACK": 36,
              "ARTIST": len({(r['track_id'], r['artist_id']) for r in tracks})}
    manifest = {"version": VERSION, "source": "Original fictional teaching fixture; build_fixture.py",
                "source_playlist_id": "P01", "csv_rows": {"tracks.csv":len(tracks),"playlists.csv":len(playlists)},
                "sha256": {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['tracks.csv','playlists.csv']},
                "expected_graph": counts, "duplicate_policy":"Collapse identical playlist/track/position tuples; preserve different positions and all artist credits."}
    (ROOT/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")


if __name__ == "__main__":
    build()
