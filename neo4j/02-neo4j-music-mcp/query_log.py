"""Print the Cypher statements a Neo4j instance received, read from its query.log.

    uv run --frozen python query_log.py [--log PATH] [--last N] [--since TIME]
                                        [--app TEXT | --all] [--explain] [--started]

The Enterprise edition that Neo4j Desktop installs writes logs/query.log by
default (db.logs.query.enabled=VERBOSE): one "Query started" entry and one
completion entry per statement, with the statement text, the database, the
user, and the client's metadata. A statement may span several lines. This
script prints one block per completed statement: local time, outcome,
database, user, client application, elapsed time, transaction id, and the
statement. By default it shows only statements sent by the Neo4j MCP server
(client metadata app 'MCP4NEO4J/...') and hides the EXPLAIN that the server
runs before each read to confirm it is read-only. Nothing here talks to the
database; the file is the database's own record of what it executed.
"""
import argparse
from datetime import datetime
from pathlib import Path
import re
import sys

DESKTOP_LOGS = Path.home() / 'Library/Application Support/neo4j-desktop/Application/Data/dbmss'
HEADER = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{4}) +(INFO|WARN|ERROR) +(Query started: )?'
                    r'id:(\d+) - transaction id:(-?\d+) - (\d+) ms: \(planning: \d+, waiting: \d+\) - (.*?)>\t(.*)$', re.DOTALL)


def find_log(explicit):
    if explicit:
        return Path(explicit)
    candidates = sorted(DESKTOP_LOGS.glob('dbms-*/logs/query.log'))
    if len(candidates) == 1:
        return candidates[0]
    hint = 'In Desktop\'s Query tool, SHOW SETTINGS YIELD name, value WHERE name = \'server.directories.logs\' RETURN value prints the logs directory.'
    if not candidates:
        raise SystemExit('No query.log found under ' + str(DESKTOP_LOGS) + '; pass --log PATH. ' + hint)
    raise SystemExit('Several instances found; pass --log PATH, one of:\n  ' + '\n  '.join(map(str, candidates)))


def entries(lines):
    """Yield one dict per log entry; continuation lines belong to the entry above them."""
    current = None
    for line in lines:
        if HEADER.match(line.rstrip('\n')) and not (current and current['open_braces']):
            if current:
                yield finish(current)
            current = {'lines': [line.rstrip('\n')], 'open_braces': 0}
        elif current:
            current['lines'].append(line.rstrip('\n'))
    if current:
        yield finish(current)


def finish(raw):
    text = '\n'.join(raw['lines'])
    m = HEADER.match(text)
    stamp, level, started, qid, tx, elapsed, source, tail = m.groups()
    when = datetime.strptime(stamp, '%Y-%m-%d %H:%M:%S.%f%z').astimezone()
    client = source.split('\t')[2] if source.count('\t') >= 2 else source
    runtime_at = tail.rfind(' - runtime=')
    before, after = (tail[:runtime_at], tail[runtime_at + len(' - runtime='):]) if runtime_at >= 0 else (tail, '')
    database, user, rest = (before.split(' - ', 2) + ['', ''])[:3]
    params_at = rest.rfind(' - {')
    statement, params = (rest[:params_at], rest[params_at + 3:]) if params_at >= 0 else (rest, '')
    runtime, _, meta_and_error = after.partition(' - ')
    meta_end = meta_and_error.find('}')
    meta = meta_and_error[:meta_end + 1] if meta_end >= 0 else meta_and_error
    error = meta_and_error[meta_end + 1:].lstrip(' -') if meta_end >= 0 else ''
    app = re.search(r"app: '([^']*)'", meta)
    return {'when': when, 'level': level, 'started': bool(started), 'id': int(qid), 'tx': int(tx), 'elapsed_ms': int(elapsed),
            'client': client, 'database': database, 'user': user, 'statement': statement.strip(), 'params': params,
            'runtime': runtime, 'app': app.group(1) if app else '', 'error': error}


def select(records, app, include_explain, include_started, since):
    for r in records:
        if r['started'] and not include_started:
            continue
        if app is not None and app not in r['app']:
            continue
        if not include_explain and r['statement'].upper().startswith('EXPLAIN'):
            continue
        if since and r['when'] < since:
            continue
        yield r


def render(r):
    outcome = 'started' if r['started'] else ('fail' if r['level'] == 'ERROR' else 'success')
    head = f"{r['when'].strftime('%Y-%m-%d %H:%M:%S %z')}  {outcome:7}  {r['database']}  {r['user']}  {r['app'] or r['client']}  {r['elapsed_ms']} ms  tx {r['tx']}"
    body = '\n'.join('    ' + line for line in r['statement'].splitlines())
    if r['params'] and r['params'] != '{}':
        body += '\n    params: ' + r['params']
    if r['error']:
        body += '\n    error: ' + r['error']
    return head + '\n' + body


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--log', help='path to query.log (default: the single Desktop instance on macOS)')
    parser.add_argument('--last', type=int, default=50, help='show the last N statements (0 = all); default 50')
    parser.add_argument('--since', help='local time, e.g. 2026-11-18T16:30; show statements at or after it')
    parser.add_argument('--app', default='MCP4NEO4J', help="client application to show (default MCP4NEO4J, the Neo4j MCP server)")
    parser.add_argument('--all', action='store_true', help='show every client, including Desktop\'s Query tool')
    parser.add_argument('--explain', action='store_true', help="include the server's EXPLAIN pre-checks")
    parser.add_argument('--started', action='store_true', help='include "Query started" entries, not only completions')
    args = parser.parse_args()
    path = find_log(args.log)
    since = datetime.fromisoformat(args.since).astimezone() if args.since else None
    with path.open(encoding='utf-8', errors='replace') as handle:
        chosen = list(select(entries(handle), None if args.all else args.app, args.explain, args.started, since))
    if args.last:
        chosen = chosen[-args.last:]
    print(f'# {path}\n# {len(chosen)} statement(s)' + ('' if args.all else f" from client app containing '{args.app}'") + '\n')
    for r in chosen:
        print(render(r) + '\n')


if __name__ == '__main__':
    main()
