import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
from music_data import ROOT, FIXTURE, read_fixture, graph_counts, expected_answers


def test_fixture_contract():
    manifest, tracks, playlists=read_fixture()
    assert graph_counts(tracks,playlists)==manifest['expected_graph']
    assert len(tracks)==48 and len(playlists)==92
    assert len({(r['playlist_id'],r['track_id'],r['position']) for r in playlists})==89
    assert len({r['track_id'] for r in playlists if r['playlist_id']=='P01'})==10
    assert len({r['position'] for r in playlists if r['playlist_id']=='P01'})==11
    assert len({r['artist_id'] for r in tracks if r['track_id']=='T01'})==2


def test_original_generator_deterministic(tmp_path):
    spec=importlib.util.spec_from_file_location('fixture_builder',FIXTURE/'build_fixture.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.ROOT=tmp_path;module.build()
    for name in ['tracks.csv','playlists.csv','manifest.json']:
        assert (tmp_path/name).read_bytes()==(FIXTURE/name).read_bytes()


def test_corrupted_fixture_rejected(tmp_path):
    for p in FIXTURE.glob('*'):
        if p.is_file():shutil.copy(p,tmp_path/p.name)
    with (tmp_path/'tracks.csv').open('a') as stream:stream.write('corrupt\n')
    with pytest.raises(ValueError,match='hash mismatch'):
        read_fixture(tmp_path)


def test_hand_computed_semantics():
    # Three paths to artist A, two playlists. Duplicate rows must not inflate counts.
    tracks=[{'track_id':'T1','artist_id':'A','artist_name':'Artist'},
            {'track_id':'T2','artist_id':'A','artist_name':'Artist'},
            {'track_id':'T1','artist_id':'B','artist_name':'Guest'}]
    playlists=[{'playlist_id':'P1','playlist_name':'Same','track_id':'T1'},
               {'playlist_id':'P1','playlist_name':'Same','track_id':'T2'},
               {'playlist_id':'P2','playlist_name':'Same','track_id':'T1'}]
    result=expected_answers(tracks,playlists,'P1')
    assert result['question_a']==[{'artist_id':'A','artist_name':'Artist','playlist_count':2},
                                  {'artist_id':'B','artist_name':'Guest','playlist_count':2}]
    assert result['question_b']==[{'playlist_id':'P2','playlist_name':'Same','shared_tracks':1}]
    assert expected_answers(tracks+tracks,playlists+playlists,'P1')==result


def test_fixture_rankings_and_duplicate_invariance():
    _,tracks,playlists=read_fixture()
    result=expected_answers(tracks,playlists)
    assert expected_answers(tracks,playlists+playlists)==result
    for key,count,idkey in [('question_a','playlist_count','artist_id'),('question_b','shared_tracks','playlist_id')]:
        rows=result[key]
        assert rows==sorted(rows,key=lambda r:(-r[count],r[idkey]))
        assert 1<=len(rows)<=5
        assert len({r[count] for r in rows})<len(rows)  # fixture really exercises tie order
    assert all(r['playlist_id']!='P01' for r in result['question_b'])
    with pytest.raises(ValueError,match='Unknown source'):
        expected_answers(tracks,playlists,'absent')


def test_missing_credentials_diagnostic():
    import os
    env={k:v for k,v in os.environ.items() if not k.startswith('NEO4J_MCP_')}
    result=subprocess.run([sys.executable,str(ROOT/'database.py'),'check'],env=env,capture_output=True,text=True,timeout=30)
    assert result.returncode!=0
    assert result.stdout==''
    assert 'NEO4J_MCP_PASSWORD' in result.stderr


def test_config_template_is_the_general_stdio_entry():
    server=json.loads((ROOT/'.mcp.json.example').read_text())['mcpServers']['neo4j']
    assert server['type']=='stdio' and server['command']=='uvx' and server['args']==['neo4j-mcp-server@2.1.1']
    assert server['env']['NEO4J_MCP_PASSWORD']=='${NEO4J_MCP_PASSWORD}'
    assert server['env']['NEO4J_MCP_DATABASE']=='music'
    assert server['env']['NEO4J_MCP_READ_ONLY']=='true'


def test_settings_allow_only_the_read_tools():
    permissions=json.loads((ROOT/'.claude/settings.json').read_text())['permissions']
    assert set(permissions['allow'])=={'mcp__neo4j__get-schema','mcp__neo4j__read-cypher'}
    assert 'deny' not in permissions


def test_student_export_excludes_answers_and_local_state(tmp_path):
    from export_students import export
    target=export(tmp_path/'student')
    assert (target/'uv.lock').is_file()
    assert not (target/'evidence/live.json').exists()
    assert not (target/'.venv').exists()
    assert (target/'.claude/settings.json').is_file()
    assert not (target/'launch_server.py').exists()
    assert not list(target.rglob('expected-answers.json'))
    assert not list(target.rglob('.env'))
    with pytest.raises(ValueError,match='empty'):
        export(target)


def test_empty_overlap_is_not_a_missing_source():
    tracks=[{'track_id':'T1','artist_id':'A','artist_name':'A'},
            {'track_id':'T2','artist_id':'B','artist_name':'B'}]
    playlists=[{'playlist_id':'P1','playlist_name':'One','track_id':'T1'},
               {'playlist_id':'P2','playlist_name':'Two','track_id':'T2'}]
    assert expected_answers(tracks,playlists,'P1')['question_b']==[]


def test_reset_rejects_foreign_database():
    from database import matches_fixture
    class Session:
        def run(self, query):
            return [{'labels':['Personal'],'properties':{'id':'secret'}}]
    _,tracks,playlists=read_fixture()
    assert not matches_fixture(Session(),tracks,playlists)
