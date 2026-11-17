MATCH (p:Playlist)-[:HAS_TRACK]->(:Track)-[:ARTIST]->(a:Artist)
RETURN a.id AS artist_id, a.name AS artist_name, count(DISTINCT p) AS playlist_count
ORDER BY playlist_count DESC, artist_id ASC
LIMIT 5
