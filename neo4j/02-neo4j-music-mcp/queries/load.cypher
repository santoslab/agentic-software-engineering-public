CREATE CONSTRAINT music_track_id IF NOT EXISTS FOR (n:Track) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT music_artist_id IF NOT EXISTS FOR (n:Artist) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT music_album_id IF NOT EXISTS FOR (n:Album) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT music_playlist_id IF NOT EXISTS FOR (n:Playlist) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT music_user_id IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE;
UNWIND $tracks AS row
MERGE (t:Track {id:row.track_id}) SET t.name=row.track_name
MERGE (a:Artist {id:row.artist_id}) SET a.name=row.artist_name
MERGE (l:Album {id:row.album_id}) SET l.name=row.album_name
MERGE (l)-[:HAS_TRACK]->(t)
MERGE (t)-[:ARTIST]->(a);
UNWIND $playlists AS row
MATCH (t:Track {id:row.track_id})
MERGE (p:Playlist {id:row.playlist_id}) SET p.name=row.playlist_name
MERGE (u:User {id:row.user_id})
MERGE (u)-[:OWNS]->(p)
MERGE (p)-[:HAS_TRACK {position:row.position}]->(t);
