# DevX Gateway Assistant - Enterprise Integration Guide

## Overview
This guide provides step-by-step instructions for integrating the DevX Gateway Assistant into your existing enterprise DevX Agent infrastructure, following Wells Fargo enterprise standards.

## Prerequisites
- Existing DevX Agent infrastructure (Orchestra Version Automation service)
- Access to enterprise GitHub repositories
- MCP-compatible IDE (VS Code with DevX Extension, Cursor, etc.)

## Integration Steps

### Step 1: Repository Setup
Ensure your repository follows the enterprise structure:

```
devx-gateway-enterprise/
├── docs/
│   └── gateway/
│       ├── index/
│       │   └── prompt.md          # Intent mapping for DevX Agent
│       ├── nfr/
│       │   └── security-controls.md
│       └── workflows/
│           └── gateway-assistant.md
├── data/
│   └── gateway/
│       ├── index.csv              # Documentation registry
│       └── workflows/
│           └── gateway-assistant.json
└── server/
    ├── mcp_server.py              # MCP server entry point
    └── main.py                    # FastAPI tools implementation
```

### Step 2: DevX Agent Configuration
Contact your DevX Agent team with the following details:

**Required Information:**
- **Repo URL:** `https://github.com/wftgitsas-CHIEF-TECH-OFC/devx-gateway-enterprise`
- **Branch:** `main`
- **Prompt file path:** `/docs/gateway/index/prompt.md`
- **Index file path:** `/data/gateway/index.csv`

**Outcome:** The DevX Agent team will configure Orchestra Version Automation service to read through your documentation.

### Step 3: MCP Server Deployment
Deploy the MCP server to your enterprise environment:

```bash
# Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run MCP server
python server/mcp_server.py
```

The server will be available at `http://localhost:8765` with the following endpoints:
- `/.well-known/mcp.json` - MCP manifest for auto-discovery
- `/tools/*` - All gateway assistant tools

### Step 4: Enterprise MCP Configuration
Update your IDE's MCP configuration to include:

```json
{
  "mcpServers": {
    "devx-gateway": {
      "command": "python",
      "args": ["server/mcp_server.py"],
      "cwd": "/path/to/devx-gateway-enterprise"
    }
  }
}
```

### Step 5: Testing Integration
Use the provided test suite to verify integration:

```bash
# Run the test flow
cd test_folder
./test_flow.sh

# Or use Postman collection
# Import: test_folder/DevX_Gateway_MCP.postman_collection.json
```

## Enterprise Standards Compliance

### Documentation Structure
✅ **Prompt File:** `/docs/gateway/index/prompt.md` - Maps user queries to specific responses
✅ **Index File:** `/data/gateway/index.csv` - Registry of documentation topics
✅ **Workflow JSON:** `/data/gateway/workflows/gateway-assistant.json` - Step-by-step instructions

### MCP Integration
✅ **Manifest:** `/.well-known/mcp.json` - Auto-discovery endpoint
✅ **Tools:** 7 enterprise-ready tools for gateway workflow
✅ **CORS:** Configured for enterprise IDE integration

### Security & Compliance
✅ **Guardrails:** Built-in security control synthesis
✅ **Policy Engine:** OPA-based validation
✅ **Audit Trail:** Complete workflow tracking

## Usage Examples

### Via DevX Agent (Enterprise)
Users can now ask questions like:
- "Decide the right API gateway for my payments service"
- "Generate proxy bundle from my OAS with security guardrails"
- "Build API proxy with required bank guardrails"

The DevX Agent will route these to the appropriate gateway assistant tools.

### Via MCP Direct (Development)
Developers can use the MCP tools directly:
- `discover_oas` - Find OpenAPI specs
- `analyze_oas` - Extract API traits
- `decide_gateway` - Choose Apigee vs DataPower
- `synthesize_guardrails` - Create security plan
- `generate_bundle` - Build proxy artifacts
- `opa_gate` - Validate controls
- `run_gateway_assistant` - End-to-end workflow

## Support
For integration support, contact your DevX Agent team using the available enterprise support channels.

## File Structure Summary
- `docs/gateway/index/prompt.md` - Intent mapping (follows enterprise Angular prompt.md pattern)
- `data/gateway/index.csv` - Documentation registry (follows enterprise index.csv pattern)
- `data/gateway/workflows/gateway-assistant.json` - Workflow instructions
- `server/mcp_server.py` - MCP server entry point
- `mcp.json` - MCP manifest for auto-discovery
