# DevX Gateway Assistant (Enterprise-Ready)
A structured project that plugs into your DevX Agent to implement shift-left API gateway selection and proxy generation inside the IDE.

Flow: VS Code (DevX) → docs/gateway/index/prompt.md → data/gateway/index.csv → data/gateway/workflows/gateway-assistant.json → MCP Server (/server) → .out/* artifacts.
# aiagentAIMgmt

## Running as MCP Server

To let DevX Agent (VS Code MCP extension, Cursor, etc.) auto-discover this server:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server/mcp_server.py

