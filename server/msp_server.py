import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up from /server to project root

from main import app as tools_app

# Wrap existing FastAPI app as MCP-compatible
mcp_app = FastAPI(title="DevX Gateway MCP Server")

# Allow IDEs to call this locally
mcp_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@mcp_app.get("/.well-known/mcp.json")
async def mcp_manifest():
    """Expose MCP manifest for discovery by clients."""
    manifest_path = os.path.join(BASE_DIR, "mcp.json")
    with open(manifest_path) as f:
        return JSONResponse(json.load(f))

# Mount the existing tools FastAPI app under /tools
mcp_app.mount("/tools", tools_app)

if __name__ == "__main__":
    uvicorn.run("msp_server:mcp_app", host="0.0.0.0", port=8765, reload=True)
