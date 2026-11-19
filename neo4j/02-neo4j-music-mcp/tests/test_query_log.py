"""query_log.py parses the Enterprise query.log format: multi-line statements, EXPLAIN pre-checks, errors, clients."""
import io
from datetime import datetime, timedelta, timezone

from query_log import entries, select, render

TAB = '\t'
HEAD = '2026-11-18 22:49:30.{ms}+0000 {level}  {started}id:{qid} - transaction id:{tx} - {ms_el} ms: (planning: 12, waiting: 0) - 0 B - 45 page hits, 0 page faults - bolt-session' + TAB + 'bolt' + TAB + '{driver}' + TAB + TAB + 'client/127.0.0.1:58439' + TAB + 'server/127.0.0.1:7687>' + TAB
TAIL = " - {params} - runtime={runtime} - {meta}{error}"
MCP = "{app: 'MCP4NEO4J/2.1.1'}"

def line(level='INFO', started='', qid=13, tx=12, ms='430', ms_el=325, driver='Go Driver/6.4.0', db='music', stmt='RETURN 1', params='{}', runtime='pipelined', meta=MCP, error=''):
    return HEAD.format(ms=ms, level=level, started=started, qid=qid, tx=tx, ms_el=ms_el, driver=driver) + f'{db} - neo4j - ' + stmt + TAIL.format(params=params, runtime=runtime, meta=meta, error=error)

WRITE = "MATCH (u:User {id: 'U01'})\nMERGE (p:Playlist {id: 'P09'})\n  SET p.name = 'Class Demo'\nRETURN p.id AS playlist"
LOG = '\n'.join([
    line(started='Query started: ', qid=11, tx=10, ms='100', stmt="EXPLAIN MATCH (t:Track) RETURN count(t)", runtime='null'),
    line(qid=11, tx=10, ms='120', stmt="EXPLAIN MATCH (t:Track) RETURN count(t)", runtime='slotted'),
    line(started='Query started: ', qid=12, tx=11, ms='130', stmt="MATCH (t:Track) RETURN count(t)", runtime='null'),
    line(qid=12, tx=11, ms='140', stmt="MATCH (t:Track) RETURN count(t)"),
    line(started='Query started: ', qid=13, tx=12, ms='200', stmt=WRITE, runtime='null'),
    line(qid=13, tx=12, ms='430', stmt=WRITE),
    line(level='ERROR', qid=14, tx=-1, ms='500', db='<none>', stmt='RETURN gds.version() as gdsVersion', runtime='null', error=" - Unknown function 'gds.version' (line 1, column 8 (offset: 7))"),
    line(qid=15, tx=3586, ms='600', driver='neo4j-javascript/6.0.1', db='system', stmt='SHOW DATABASES YIELD *;', runtime='system', meta="{app: 'nx', container_app: 'workspace', type: 'system', vendor: 'neo4j'}"),
    line(qid=16, tx=13, ms='700', stmt="CALL apoc.meta.schema({sample: $sampleSize}) YIELD value RETURN value", params='{sampleSize: 100}'),
]) + '\n'


def parsed(**kw):
    defaults = dict(app='MCP4NEO4J', include_explain=False, include_started=False, since=None)
    defaults.update(kw)
    return list(select(entries(io.StringIO(LOG)), **defaults))


def test_entries_reassemble_multiline_statements_and_fields():
    records = list(entries(io.StringIO(LOG)))
    assert len(records) == 9
    write = [r for r in records if r['tx'] == 12 and not r['started']][0]
    assert write['statement'] == WRITE and write['database'] == 'music' and write['user'] == 'neo4j'
    assert write['app'] == 'MCP4NEO4J/2.1.1' and write['elapsed_ms'] == 325 and write['level'] == 'INFO'
    assert write['when'].astimezone(timezone.utc) == datetime(2026, 11, 18, 22, 49, 30, 430000, tzinfo=timezone.utc)


def test_default_selection_hides_explain_started_and_other_clients():
    statements = [r['statement'] for r in parsed()]
    assert statements == ['MATCH (t:Track) RETURN count(t)', WRITE, 'RETURN gds.version() as gdsVersion',
                          'CALL apoc.meta.schema({sample: $sampleSize}) YIELD value RETURN value']
    assert [r['statement'] for r in parsed(include_explain=True)][0].startswith('EXPLAIN')
    assert len(parsed(include_started=True)) == 6  # two reads, the write, both with start entries; the error; the schema call
    assert any(r['app'] == 'nx' for r in parsed(app=None))


def test_errors_params_and_since_are_reported():
    failure = [r for r in parsed() if r['level'] == 'ERROR'][0]
    assert failure['error'].startswith("Unknown function 'gds.version'") and failure['database'] == '<none>' and failure['tx'] == -1
    schema = [r for r in parsed() if 'apoc.meta.schema' in r['statement']][0]
    assert schema['params'] == '{sampleSize: 100}'
    text = render(schema)
    assert 'params: {sampleSize: 100}' in text and '  success  music  neo4j  MCP4NEO4J/2.1.1' in text
    assert 'fail' in render(failure) and "error: Unknown function" in render(failure)
    late = datetime(2026, 11, 18, 22, 49, 30, 450000, tzinfo=timezone.utc)
    assert [r['tx'] for r in parsed(since=late)] == [-1, 13]
