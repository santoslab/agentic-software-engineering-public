"""Compare real direct queries and official MCP calls with the CSV oracle."""
import asyncio
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

from mcp import Client
from mcp.client.stdio import StdioServerParameters
from neo4j import GraphDatabase

from database import counts, settings, matches_fixture
from music_data import ROOT, read_fixture, expected_answers


async def run(output):
    manifest, tracks, playlists=read_fixture()
    expected=expected_answers(tracks,playlists)
    queries={key:(ROOT/'queries'/name).read_text() for key,name in [('question_a','question-a.cypher'),('question_b','question-b.cypher')]}
    uri,auth,database=settings()
    with GraphDatabase.driver(uri,auth=auth) as driver:
        with driver.session(database=database) as session:
            version=session.run('CALL dbms.components() YIELD versions,edition RETURN versions[0] AS version,edition').single().data()
            observed_counts=counts(session)
            assert observed_counts==manifest['expected_graph']
            assert matches_fixture(session,tracks,playlists), 'Graph identity differs from fixture'
            direct={key:session.run(query).data() for key,query in queries.items()}
            assert direct==expected
    # Stdio transport only inherits a limited environment; explicitly supply provider variables.
    env={key:val for key,val in os.environ.items() if key.startswith('NEO4J_MCP_')}
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'launch_server.py')],env=env)
    async with Client(params,read_timeout_seconds=30) as client:
        listing=await client.list_tools()
        assert {t.name for t in listing.tools}=={'get-schema','read-cypher'}
        calls=[]
        for name,args in [('get-schema',{})]+[('read-cypher',{'query':query}) for query in queries.values()]:
            result=await client.call_tool(name,args)
            calls.append({'name':name,'arguments':args,'result':result.model_dump(mode='json',by_alias=True,exclude_none=True)})
            assert not result.is_error, str(result.content)
            if name=='read-cypher':
                key=list(queries)[len(calls)-2]
                returned=json.loads(''.join(block.text for block in result.content if block.type=='text'))
                assert returned==expected[key], 'MCP results differ from CSV oracle'
        report={'captured_at':datetime.now(timezone.utc).isoformat(),'kind':'LLM-free real Neo4j driver and MCP subprocess',
                'fixture':manifest['version'],'database_version':version,'protocol_version':client.session.protocol_version,
                'counts':observed_counts,'direct_results':direct,
                'tools':listing.model_dump(mode='json',by_alias=True,exclude_none=True),'calls':calls}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(report,indent=2)+'\n')
    print('Direct reference queries agree with CSV oracle; schema/read MCP calls succeeded. Evidence: '+str(output))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',default='evidence/live.json')
    args=parser.parse_args()
    asyncio.run(run(args.output))
