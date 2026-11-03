"""Offline CLI evaluation of pinned Task Master; synthetic data only."""
import concurrent.futures
import json
import os
import platform
from pathlib import Path
import statistics
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parent
CLI = ROOT / 'node_modules/task-master-ai/dist/task-master.js'
ENV = {k: os.environ[k] for k in ('PATH', 'HOME', 'TMPDIR', 'LANG') if k in os.environ}
ENV.update(NO_COLOR='1', CI='1')
RESULTS = {'version': '0.43.1', 'platform': platform.platform(),
           'node': subprocess.check_output(['node', '--version'], text=True).strip(),
           'method': 'Fresh CLI process per call; warm filesystem cache; three samples; '
                     'synthetic sparse DAG, half done, no subtasks; local JSON only.',
           'backlogs': [], 'concurrency': []}


def seed(name, count):
    project = ROOT / name
    base = project / '.taskmaster'
    (base / 'tasks').mkdir(parents=True, exist_ok=True)
    (base / 'config.json').write_text(json.dumps({
        'storage': {'type': 'file'},
        'global': {'anonymousTelemetry': False, 'logLevel': 'error'}
    }))
    tasks = [dict(id=str(i), title=f'Synthetic task {i}',
                  description='Implement a bounded change following the specification. ' * 4,
                  status='done' if i % 2 else 'pending', priority='medium',
                  dependencies=[str(i-1)] if i % 2 == 0 else [],
                  details='Context, implementation notes, relevant files, and progress. ' * 16,
                  testStrategy='Run focused tests and record the command, result, and remaining work. ' * 4,
                  subtasks=[]) for i in range(1, count+1)]
    datafile = base / 'tasks/tasks.json'
    datafile.write_text(json.dumps({'master': {'tasks': tasks, 'metadata': {}}}, indent=2))
    return project, datafile


def run(project, args, barrier=None):
    if barrier:
        barrier.wait(timeout=30)
    start = time.perf_counter()
    p = subprocess.run(['node', str(CLI), *args], cwd=project, env=ENV,
                       capture_output=True, text=True, timeout=45)
    elapsed = time.perf_counter() - start
    # The CLI can print a migration notice before JSON.
    start_json = p.stdout.find('{\n')
    parsed = None
    if start_json >= 0:
        parsed = json.JSONDecoder().raw_decode(p.stdout[start_json:])[0]
    return {'seconds': elapsed, 'returncode': p.returncode,
            'stdout_bytes': len(p.stdout.encode()), 'json': parsed,
            'stderr': p.stderr[-2000:]}


def checked(project, args):
    result = run(project, args)
    assert result['returncode'] == 0, result
    assert isinstance(result['json'], dict), result
    return result


def save():
    (ROOT / 'results.json').write_text(json.dumps(RESULTS, indent=2))


for count in (100, 1000, 10000):
    project, datafile = seed(f'backlog-{count}', count)
    entry = {'tasks': count, 'input_bytes': datafile.stat().st_size, 'commands': {}}
    for operation in ('show', 'next', 'set-status'):
        samples = []
        for sample in range(3):
            if operation == 'show':
                args = ['show', str(count), '--json']
            elif operation == 'next':
                args = ['next', '--format', 'json']
            else:
                status = 'in-progress' if sample % 2 == 0 else 'pending'
                args = ['set-status', str(count), status, '--format', 'json']
            result = checked(project, args)
            if operation in ('show', 'next'):
                assert str(result['json']['task']['id']) == (str(count) if operation == 'show' else '2')
            else:
                assert result['json']['success'] is True
                current = json.loads(datafile.read_text())['master']['tasks']
                assert current[-1]['status'] == status
                assert sum(t['status'] == 'done' for t in current) == count // 2
            samples.append(result['seconds'])
        entry['commands'][operation] = {
            'median_seconds': statistics.median(samples), 'samples_seconds': samples,
            'stdout_bytes': result['stdout_bytes']}
        print(json.dumps({'backlog': count, 'operation': operation,
                          **entry['commands'][operation]}), flush=True)
    listing = checked(project, ['list', '--ready', '--json'])
    assert len(listing['json']['tasks']) == count // 2
    entry['ready_list'] = {'seconds': listing['seconds'],
                           'tasks_returned': len(listing['json']['tasks']),
                           'stdout_bytes': listing['stdout_bytes']}
    RESULTS['backlogs'].append(entry)
    save()

for count, writers, rounds in ((1000, 2, 3), (1000, 8, 3), (10000, 8, 3)):
    for repeat in range(rounds):
        project, datafile = seed(f'concurrent-{count}-{writers}-{repeat}', count)
        ids = [str(2 * i) for i in range(1, writers + 1)]
        barrier = threading.Barrier(writers)
        start = time.perf_counter()
        with concurrent.futures.ThreadPoolExecutor(max_workers=writers) as pool:
            jobs = [pool.submit(run, project,
                                ['set-status', task_id, 'in-progress', '--format', 'json'],
                                barrier) for task_id in ids]
            outputs = [job.result() for job in jobs]
        data = json.loads(datafile.read_text())['master']['tasks']
        persisted = [t['id'] for t in data if t['status'] == 'in-progress']
        assert len(data) == count
        assert set(persisted).issubset(ids)
        outcome = {'tasks': count, 'writers': writers, 'repeat': repeat + 1,
                   'seconds': time.perf_counter() - start,
                   'commands_reported_success': sum(r['returncode'] == 0 and
                       r['json'] is not None and r['json'].get('success') is True for r in outputs),
                   'updates_persisted': len(persisted), 'expected_ids': ids,
                   'persisted_ids': persisted, 'outputs': outputs}
        RESULTS['concurrency'].append(outcome)
        save()
        print(json.dumps({k: v for k, v in outcome.items() if k != 'outputs'}), flush=True)

project, datafile = seed('reservation', 100)
before = datafile.read_bytes()
first = checked(project, ['next', '--format', 'json'])['json']['task']['id']
checked(project, ['set-status', first, 'in-progress', '--format', 'json'])
after_status = datafile.read_bytes()
second = checked(project, ['next', '--format', 'json'])['json']['task']['id']
assert after_status == datafile.read_bytes(), 'next unexpectedly wrote the backlog'
RESULTS['reservation'] = {'first_next': first, 'next_after_marking_in_progress': second,
                          'next_changed_file': False}
save()
print(json.dumps({'reservation': RESULTS['reservation']}), flush=True)

# Sequential control distinguishes concurrent loss from fixture/schema problems.
project, datafile = seed('sequential-control', 1000)
for task_id in ('2', '4'):
    checked(project, ['set-status', task_id, 'in-progress', '--format', 'json'])
persisted = [t['id'] for t in json.loads(datafile.read_text())['master']['tasks']
             if t['status'] == 'in-progress']
assert persisted == ['2', '4'], persisted
RESULTS['sequential_control'] = {'commands_reported_success': 2, 'persisted_ids': persisted}
save()
print(json.dumps({'sequential_control': RESULTS['sequential_control']}), flush=True)
