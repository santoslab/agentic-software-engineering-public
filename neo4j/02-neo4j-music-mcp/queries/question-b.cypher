MATCH (source:Playlist {id:'P01'})-[:HAS_TRACK]->(t:Track)<-[:HAS_TRACK]-(other:Playlist)
WHERE other <> source
RETURN other.id AS playlist_id, other.name AS playlist_name, count(DISTINCT t) AS shared_tracks
ORDER BY shared_tracks DESC, playlist_id ASC
LIMIT 5
