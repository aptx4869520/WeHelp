# Week 7 Assignment

## Task 1 - Generate Access Token

- Added token column to member table
- Added PUT /api/token
- Generated token using hashlib SHA256
- Bound token to logged-in member
- Added token generation UI

## Task 2 - MCP Server and Tool

- Integrated FastMCP into FastAPI
- MCP endpoint: http://127.0.0.1:8000/mcp/
- Added Create Message Tool
- Read Bearer Token from Authorization Header
- Created messages using the token owner's member ID

## Task 3 - Codex Testing

- Tested MCP Tool with member A
- Tested MCP Tool with member B
- Confirmed correct member IDs
- Added testing screenshots