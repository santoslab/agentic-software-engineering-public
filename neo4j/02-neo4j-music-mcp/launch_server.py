"""Launch the pinned official provider with explicit homework defaults."""
import os
import sys
from database import settings

if __name__ == '__main__':
    settings()  # fail clearly on stderr before starting a protocol process
    os.environ['NEO4J_MCP_READ_ONLY']='true'
    os.environ['NEO4J_MCP_TELEMETRY']='false'
    os.environ['NEO4J_MCP_TOOLS']='get-schema,read-cypher'
    os.environ['NEO4J_MCP_TRANSPORT_MODE']='stdio'
    os.execv(sys.executable,[sys.executable,'-m','neo4j_mcp_server'])
