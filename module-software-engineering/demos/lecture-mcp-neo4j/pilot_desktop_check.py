"""Pilot check: is this Neo4j Desktop instance ready for the official MCP server?

Run from neo4j/02-neo4j-music-mcp/ so the locked environment supplies the
neo4j driver and the mcp client:

    uv run --frozen python ../../module-software-engineering/demos/lecture-mcp-neo4j/pilot_desktop_check.py

The script prompts for the database password and keeps it in memory only.
It checks, in order: driver connectivity and server version; databases;
APOC meta procedures present and executable; then launches
`uvx neo4j-mcp-server@<version>` as a stdio child in read-only and in write
mode, lists tools, and calls get-schema and a trivial read-cypher. It writes
a password-free report to --output (default: reports/pilot-report.json beside this file).
"""
import argparse
import asyncio
import getpass
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase
from neo4j.exceptions import ClientError, Neo4jError
from mcp import Client
from mcp.client.stdio import StdioServerParameters

PROVIDER_VERSION = '2.1.1'


def step(report, name, ok, detail):
    report['steps'].append({'step': name, 'ok': ok, 'detail': detail})
    print(('PASS ' if ok else 'FAIL ') + name + ': ' + str(detail))


def direct_checks(report, uri, auth, database):
    with GraphDatabase.driver(uri, auth=auth, connection_timeout=10) as driver:
        try:
            driver.verify_connectivity()
            step(report, 'connect', True, uri)
        except Exception as e:  # noqa: BLE001 - report any connectivity failure
            step(report, 'connect', False, f'{type(e).__name__}: {e}')
            return False
        with driver.session(database='system') as s:
            comp = s.run('CALL dbms.components() YIELD versions, edition RETURN versions[0] AS version, edition').single().data()
            step(report, 'server', True, comp)
            dbs = [r.data() for r in s.run('SHOW DATABASES YIELD name, currentStatus, default RETURN name, currentStatus, default')]
            step(report, 'databases', True, dbs)
            names = {d['name'] for d in dbs}
            if database not in names:
                step(report, 'target database exists', False, f'{database!r} not in {sorted(names)}; create it in Desktop or with CREATE DATABASE {database}')
        with driver.session(database=database if database in names else 'neo4j') as s:
            try:
                procs = [r['name'] for r in s.run("SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc.meta.' RETURN name ORDER BY name")]
                step(report, 'apoc.meta procedures present', bool(procs), procs if procs else 'none: install APOC from the instance plugin tab and restart')
            except Neo4jError as e:
                step(report, 'apoc.meta procedures present', False, f'{e.code}: {e.message}')
                procs = []
            try:
                value = s.run('CALL apoc.meta.schema() YIELD value RETURN value').single()['value']
                step(report, 'apoc.meta.schema executes', True, f'{len(value)} schema entries')
            except ClientError as e:
                hint = ''
                if 'sandbox' in (e.message or '').lower() or 'unrestricted' in (e.message or '').lower():
                    hint = ' -> add dbms.security.procedures.unrestricted=apoc.meta.* to the instance settings and restart'
                elif 'not found' in (e.message or '').lower() or 'no procedure' in (e.message or '').lower():
                    hint = ' -> APOC is not installed on this instance'
                step(report, 'apoc.meta.schema executes', False, f'{e.code}: {e.message}{hint}')
            try:
                rows = [r.data() for r in s.run("SHOW SETTINGS YIELD name, value WHERE name IN ['dbms.security.procedures.unrestricted','dbms.security.procedures.allowlist','server.bolt.listen_address'] RETURN name, value")]
                step(report, 'relevant settings', True, rows)
            except Neo4jError as e:
                step(report, 'relevant settings', False, f'{e.code}: {e.message}')
    return True


async def provider_checks(report, uri, auth, database, read_only):
    uvx = shutil.which('uvx')
    if not uvx:
        step(report, f'provider launch (read_only={read_only})', False, 'uvx not on PATH')
        return
    env = {k: v for k, v in os.environ.items() if k in ('PATH', 'HOME', 'TMPDIR', 'UV_CACHE_DIR')}
    env.update({
        'NEO4J_MCP_URI': uri, 'NEO4J_MCP_USERNAME': auth[0], 'NEO4J_MCP_PASSWORD': auth[1],
        'NEO4J_MCP_DATABASE': database, 'NEO4J_MCP_READ_ONLY': 'true' if read_only else 'false',
        'NEO4J_MCP_TELEMETRY': 'false', 'NEO4J_MCP_TRANSPORT_MODE': 'stdio',
    })
    params = StdioServerParameters(command=uvx, args=[f'neo4j-mcp-server@{PROVIDER_VERSION}'], env=env)
    label = f'read_only={read_only}'
    try:
        async with Client(params, read_timeout_seconds=90) as client:
            listing = await client.list_tools()
            names = sorted(t.name for t in listing.tools)
            step(report, f'provider tools/list ({label})', True, {'protocol': client.session.protocol_version, 'tools': names})
            expected_absent = 'write-cypher' not in names if read_only else 'write-cypher' in names
            step(report, f'write-cypher gating ({label})', expected_absent, names)
            if read_only:
                schema = await client.call_tool('get-schema', {})
                text = ''.join(b.text for b in schema.content if b.type == 'text')
                step(report, 'provider get-schema', not schema.is_error, text[:300] + ('...' if len(text) > 300 else ''))
                rows = await client.call_tool('read-cypher', {'query': 'RETURN 1 AS ok'})
                text = ''.join(b.text for b in rows.content if b.type == 'text')
                step(report, 'provider read-cypher RETURN 1', not rows.is_error, text.strip()[:200])
    except Exception as e:  # noqa: BLE001 - provider initialize failures are the point of this check
        step(report, f'provider session ({label})', False, f'{type(e).__name__}: {e}')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--uri', default=os.environ.get('NEO4J_MCP_URI', 'bolt://127.0.0.1:7687'))
    parser.add_argument('--user', default=os.environ.get('NEO4J_MCP_USERNAME', 'neo4j'))
    parser.add_argument('--database', default=os.environ.get('NEO4J_MCP_DATABASE', 'neo4j'))
    parser.add_argument('--output', default=str(Path(__file__).parent / 'reports' / 'pilot-report.json'))
    args = parser.parse_args()
    password = os.environ.get('NEO4J_MCP_PASSWORD') or getpass.getpass(f'Password for {args.user} at {args.uri}: ')
    auth = (args.user, password)
    report = {'captured_at': datetime.now(timezone.utc).isoformat(), 'uri': args.uri, 'user': args.user,
              'database': args.database, 'provider': f'neo4j-mcp-server@{PROVIDER_VERSION}', 'steps': []}
    if direct_checks(report, args.uri, auth, args.database):
        asyncio.run(provider_checks(report, args.uri, auth, args.database, read_only=True))
        asyncio.run(provider_checks(report, args.uri, auth, args.database, read_only=False))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(report, indent=2, default=str) + '\n')
    failed = [s['step'] for s in report['steps'] if not s['ok']]
    print('\nReport (no password) written to', args.output)
    print('All checks passed.' if not failed else 'Failed: ' + ', '.join(failed))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
