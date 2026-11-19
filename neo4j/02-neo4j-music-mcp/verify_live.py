"""Check the whole chain without a model: driver, fixture, reference queries,
then the official MCP server started exactly as .mcp.json starts it.

    uv run --frozen python verify_live.py [--output evidence/live.json]

Needs the NEO4J_MCP_* variables of SETUP.md section 3 and `uvx` on PATH. The
server (neo4j-mcp-server 2.1.1) runs as a stdio child in read-only mode; its
tool list, a get-schema call, and the two reference queries are compared with
the CSV oracle in music_data.py. The written report contains no password.
"""
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

from mcp import Client
from mcp.client.stdio import StdioServerParameters
from neo4j import GraphDatabase

from database import counts, settings, matches_fixture
from music_data import ROOT, read_fixture, expected_answers

SERVER_VERSION = '2.1.1'
READ_TOOLS = {'get-schema', 'read-cypher'}
OPTIONAL_TOOLS = {'list-gds-procedures'}  # offered only when Graph Data Science is installed


def server_version(session):
    # Neo4j 2026.x returns one row per component; take the kernel's rather than single().
    rows = [r.data() for r in session.run('CALL dbms.components() YIELD name, versions, edition RETURN name, versions[0] AS version, edition')]
    kernel = next((r for r in rows if r['name'] == 'Neo4j Kernel'), rows[0])
    return {'version': kernel['version'], 'edition': kernel['edition']}


async def run(output):
    manifest, tracks, playlists = read_fixture()
    expected = expected_answers(tracks, playlists)
    queries = {key: (ROOT/'queries'/name).read_text() for key, name in [('question_a', 'question-a.cypher'), ('question_b', 'question-b.cypher')]}
    uri, auth, database = settings()
    with GraphDatabase.driver(uri, auth=auth, connection_timeout=10) as driver:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            version = server_version(session)
            observed_counts = counts(session)
            assert observed_counts == manifest['expected_graph'], 'Counts differ from the manifest; run database.py check'
            assert matches_fixture(session, tracks, playlists), 'Graph identity differs from fixture'
            direct = {key: session.run(query).data() for key, query in queries.items()}
            assert direct == expected, 'Direct query results differ from CSV oracle'
    uvx = shutil.which('uvx')
    if not uvx:
        raise SystemExit('uvx not found on PATH; install uv (https://docs.astral.sh/uv/)')
    # The same launch as .mcp.json: uvx runs the pinned server, and the environment is its configuration.
    # The client adds PATH, HOME and the other inheritable variables itself.
    env = {'NEO4J_MCP_URI': uri, 'NEO4J_MCP_USERNAME': auth[0], 'NEO4J_MCP_PASSWORD': auth[1],
           'NEO4J_MCP_DATABASE': database, 'NEO4J_MCP_READ_ONLY': 'true', 'NEO4J_MCP_TELEMETRY': 'false'}
    params = StdioServerParameters(command=uvx, args=[f'neo4j-mcp-server@{SERVER_VERSION}'], env=env)
    async with Client(params, read_timeout_seconds=90) as client:  # the first launch downloads the server (about 10 MB)
        listing = await client.list_tools()
        names = {t.name for t in listing.tools}
        assert 'write-cypher' not in names, 'write-cypher offered although NEO4J_MCP_READ_ONLY=true'
        assert READ_TOOLS <= names <= READ_TOOLS | OPTIONAL_TOOLS, f'Unexpected tool list: {sorted(names)}'
        calls = []
        for name, args in [('get-schema', {})] + [('read-cypher', {'query': query}) for query in queries.values()]:
            result = await client.call_tool(name, args)
            calls.append({'name': name, 'arguments': args, 'result': result.model_dump(mode='json', by_alias=True, exclude_none=True)})
            assert not result.is_error, str(result.content)
            if name == 'read-cypher':
                key = list(queries)[len(calls)-2]
                returned = json.loads(''.join(block.text for block in result.content if block.type == 'text'))
                assert returned == expected[key], 'MCP results differ from CSV oracle'
        report = {'captured_at': datetime.now(timezone.utc).isoformat(), 'kind': 'LLM-free real Neo4j driver and MCP subprocess',
                  'fixture': manifest['version'], 'database': database, 'database_version': version,
                  'server': f'uvx neo4j-mcp-server@{SERVER_VERSION} (NEO4J_MCP_READ_ONLY=true)',
                  'protocol_version': client.session.protocol_version,
                  'counts': observed_counts, 'direct_results': direct,
                  'tools': listing.model_dump(mode='json', by_alias=True, exclude_none=True), 'calls': calls}
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(report, indent=2)+'\n')
    print(f'Direct reference queries agree with the CSV oracle; server tools {sorted(names)}; schema and read calls succeeded. Evidence: {output}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--output', default='evidence/live.json')
    asyncio.run(run(parser.parse_args().output))
