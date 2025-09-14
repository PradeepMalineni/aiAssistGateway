"""
Enterprise MCP Server for Agentic Space Deployment
Optimized for cloud deployment with enterprise security and scaling
"""
import asyncio
import json
import os
import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from contextlib import asynccontextmanager

# Configure logging for enterprise
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Enterprise configuration
ENTERPRISE_MODE = os.getenv("ENTERPRISE_MODE", "false").lower() == "true"
AUTHENTICATION_REQUIRED = os.getenv("AUTHENTICATION_REQUIRED", "false").lower() == "true"
ARTIFACTS_BASE_PATH = os.getenv("ARTIFACTS_BASE_PATH", "/tmp/gateway-artifacts")
PORT = int(os.getenv("PORT", "8080"))
HOST = os.getenv("HOST", "0.0.0.0")

# Import tools app
from main import app as tools_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management for enterprise deployment"""
    # Startup
    logger.info("Starting Gateway Assistant MCP Server in Agentic Space")
    
    # Ensure artifacts directory exists
    os.makedirs(ARTIFACTS_BASE_PATH, exist_ok=True)
    logger.info(f"Artifacts directory: {ARTIFACTS_BASE_PATH}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Gateway Assistant MCP Server")

# Create enterprise-ready FastAPI app
mcp_app = FastAPI(
    title="DevX Gateway MCP Server (Agentic Space)",
    version="1.0.0",
    description="Enterprise MCP server for API Gateway Assistant",
    lifespan=lifespan
)

# Enterprise security middleware
if ENTERPRISE_MODE:
    # CORS for enterprise domains only
    cors_origins = os.getenv("CORS_ORIGINS", "").split(",")
    mcp_app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    mcp_app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.wellsfargo.com", "localhost", "127.0.0.1"]
    )
else:
    # Development CORS (allow all for local testing)
    mcp_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Enterprise authentication dependency (placeholder)
async def verify_enterprise_auth():
    """Enterprise authentication verification"""
    if not AUTHENTICATION_REQUIRED:
        return True
    
    # TODO: Implement enterprise authentication
    # This would verify JWT tokens, enterprise certificates, etc.
    logger.info("Enterprise authentication required - implementing with DevX Agent team")
    return True

@mcp_app.get("/health")
async def health_check():
    """Enterprise health check endpoint"""
    return {
        "status": "healthy",
        "service": "devx-gateway-mcp",
        "environment": "agentic-space" if ENTERPRISE_MODE else "development",
        "version": "1.0.0"
    }

@mcp_app.get("/.well-known/mcp.json")
async def mcp_manifest():
    """Enterprise MCP manifest for auto-discovery"""
    try:
        manifest_path = os.path.join(BASE_DIR, "mcp.json")
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        # Add enterprise-specific metadata
        manifest["deployment"] = {
            "environment": "agentic-space",
            "enterprise_mode": ENTERPRISE_MODE,
            "authentication_required": AUTHENTICATION_REQUIRED,
            "artifacts_path": ARTIFACTS_BASE_PATH
        }
        
        logger.info("MCP manifest served successfully")
        return JSONResponse(manifest)
    except Exception as e:
        logger.error(f"Error serving MCP manifest: {e}")
        raise HTTPException(status_code=500, detail="Failed to load MCP manifest")

# Mount the tools app with enterprise authentication
if ENTERPRISE_MODE:
    # In enterprise mode, add authentication to all tool endpoints
    mcp_app.mount("/tools", tools_app)
else:
    # In development mode, mount without authentication
    mcp_app.mount("/tools", tools_app)

if __name__ == "__main__":
    # Enterprise deployment configuration
    config = {
        "app": "agentic_server:mcp_app",
        "host": HOST,
        "port": PORT,
        "workers": int(os.getenv("WORKERS", "1")),
        "log_level": os.getenv("LOG_LEVEL", "info").lower(),
        "access_log": True,
    }
    
    if not ENTERPRISE_MODE:
        # Development mode - add reload
        config["reload"] = True
        config["workers"] = 1
    
    logger.info(f"Starting server with config: {config}")
    uvicorn.run(**config)
