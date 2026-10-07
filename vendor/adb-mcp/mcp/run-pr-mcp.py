"""Launcher for pr-mcp.py: the upstream script defines the FastMCP server but
never calls mcp.run() (it is meant to be started via the `mcp run` CLI).
This wrapper loads it and starts the stdio transport."""
import importlib.util
import os
import sys

MCP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MCP_DIR)

spec = importlib.util.spec_from_file_location("pr_mcp", os.path.join(MCP_DIR, "pr-mcp.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

module.mcp.run()
