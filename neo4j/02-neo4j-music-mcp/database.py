"""Load/check/reset only an explicitly designated disposable homework database."""
import argparse
import json
import os
from neo4j import GraphDatabase
from music_data import ROOT, graph_counts, read_fixture


def settings():
    required = ['NEO4J_MCP_URI','NEO4J_MCP_USERNAME','NEO4J_MCP_PASSWORD']
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise SystemExit('Missing environment variables: ' + ', '.join(missing))
    return os.environ['NEO4J_MCP_URI'], (os.environ['NEO4J_MCP_USERNAME'], os.environ['NEO4J_MCP_PASSWORD']), os.environ.get('NEO4J_MCP_DATABASE','neo4j')


def counts(session):
    result = {r['label']:r['n'] for r in session.run('MATCH (n) UNWIND labels(n) AS label RETURN label,count(*) AS n')}
    for key, query in {
        'OWNS':'MATCH ()-[r:OWNS]->() RETURN count(r) AS n',
        'PLAYLIST_HAS_TRACK':'MATCH (:Playlist)-[r:HAS_TRACK]->(:Track) RETURN count(r) AS n',
        'ALBUM_HAS_TRACK':'MATCH (:Album)-[r:HAS_TRACK]->(:Track) RETURN count(r) AS n',
        'ARTIST':'MATCH (:Track)-[r:ARTIST]->(:Artist) RETURN count(r) AS n',
    }.items():
        result[key] = session.run(query).single()['n']
    return result


def matches_fixture(session, tracks, playlists):
    """Require exact expected properties and endpoints before deleting a fixture."""
    nodes=set()
    for label,key,name,rows in [('Track','track_id','track_name',tracks),
                               ('Artist','artist_id','artist_name',tracks),
                               ('Album','album_id','album_name',tracks),
                               ('Playlist','playlist_id','playlist_name',playlists),
                               ('User','user_id',None,playlists)]:
        for row in rows:
            properties={'id':row[key]}
            if name:properties['name']=row[name]
            nodes.add((label,json.dumps(properties,sort_keys=True)))
    actual_nodes=[]
    for row in session.run('MATCH (n) RETURN labels(n) AS labels, properties(n) AS properties'):
        if len(row['labels'])!=1:return False
        actual_nodes.append((row['labels'][0],json.dumps(row['properties'],sort_keys=True)))
    if len(actual_nodes)!=len(nodes) or set(actual_nodes)!=nodes:return False
    edges=set()
    for row in tracks:
        edges.add(('Album',row['album_id'],'HAS_TRACK','Track',row['track_id'],'{}'))
        edges.add(('Track',row['track_id'],'ARTIST','Artist',row['artist_id'],'{}'))
    for row in playlists:
        edges.add(('User',row['user_id'],'OWNS','Playlist',row['playlist_id'],'{}'))
        edges.add(('Playlist',row['playlist_id'],'HAS_TRACK','Track',row['track_id'],json.dumps({'position':row['position']},sort_keys=True)))
    actual_edges=[]
    for row in session.run('MATCH (a)-[r]->(b) RETURN labels(a)[0] AS a,a.id AS aid,type(r) AS kind,labels(b)[0] AS b,b.id AS bid,properties(r) AS properties'):
        actual_edges.append((row['a'],row['aid'],row['kind'],row['b'],row['bid'],json.dumps(row['properties'],sort_keys=True)))
    return len(actual_edges)==len(edges) and set(actual_edges)==edges


def execute(action, confirmation=None):
    manifest, tracks, playlists = read_fixture()
    uri, auth, database = settings()
    with GraphDatabase.driver(uri,auth=auth,connection_timeout=10) as driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            if action == 'load':
                if session.run('MATCH (n) RETURN count(n) AS n').single()['n']:
                    raise SystemExit('Load refused: database is not empty. Use a new disposable instance.')
                for query in (ROOT/'queries/load.cypher').read_text().split(';'):
                    if query.strip():
                        session.run(query,tracks=tracks,playlists=playlists).consume()
            elif action == 'reset':
                if confirmation != manifest['version']:
                    raise SystemExit('Reset requires --confirm-fixture ' + manifest['version'])
                if not matches_fixture(session, tracks, playlists):
                    raise SystemExit('Reset refused: database does not match the complete fixture. Inspect it in Desktop.')
                session.run('MATCH (n) DETACH DELETE n').consume()
                print('Reset complete; constraints retained.');return
            observed=counts(session)
            expected=graph_counts(tracks,playlists)
            if observed != expected:
                raise SystemExit('Readiness mismatch: ' + json.dumps({'expected':expected,'observed':observed}))
            print(json.dumps({'fixture':manifest['version'],'database':database,'counts':observed},indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['load','check','reset'])
    parser.add_argument('--confirm-fixture')
    args=parser.parse_args()
    execute(args.action,args.confirm_fixture)
