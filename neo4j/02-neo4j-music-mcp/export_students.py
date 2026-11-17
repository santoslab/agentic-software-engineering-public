"""Copy the explicit student package; exclude local environments and instructor evidence."""
import argparse
from pathlib import Path
import shutil
from music_data import ROOT

FILES=['README.md','SETUP.md','LICENSE-MIT','LICENSE-CC-BY-4.0','PRIMER.md','EVIDENCE.md','.mcp.json.example','.gitignore',
       'pyproject.toml','uv.lock','export_students.py','music_data.py','database.py','launch_server.py','verify_live.py']
TREES={'fixture':['build_fixture.py','tracks.csv','playlists.csv','manifest.json','PROVENANCE.md'],
       'queries':['load.cypher','question-a.cypher','question-b.cypher'],
       'tests':['test_music.py'], 'assets':['music-graph.svg']}


def export(destination):
    destination=Path(destination)
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Export destination must be absent or empty')
    destination.mkdir(parents=True,exist_ok=True)
    for name in FILES:
        shutil.copy2(ROOT/name,destination/name)
    for directory,names in TREES.items():
        (destination/directory).mkdir()
        for name in names:shutil.copy2(ROOT/directory/name,destination/directory/name)
    (destination/'evidence').mkdir()
    return destination


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('destination')
    print(export(parser.parse_args().destination))
