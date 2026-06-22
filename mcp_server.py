import os
import uvicorn
from fastapi import FastAPI, Request
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent

server = Server("Contract-Database")

MOCK_CONTRACT_REGISTRY = {
    "acme_corp": {
        "vendor_name": "Acme Industrial Logistics",
        "max_allowable_unit_price": 150.00,
        "approved_categories": ["shipping", "freight", "logistics"]
    },
    "globex_media": {
        "vendor_name": "Globex Media Substrates",
        "max_allowable_unit_price": 45.50,
        "approved_categories": ["marketing", "advertising", "print"]
    }
}

@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="verify_contract_terms",
            description="Queries the secure contract database to retrieve baseline pricing caps.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vendor_id": {"type": "string"}
                },
                "required": ["vendor_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    if name == "verify_contract_terms":
        vendor_id = arguments.get("vendor_id", "").lower()
        if vendor_id in MOCK_CONTRACT_REGISTRY:
            return [TextContent(type="text", text=f"[MATCH FOUND] Contract Parameters: {MOCK_CONTRACT_REGISTRY[vendor_id]}")]
        return [TextContent(type="text", text=f"[ALERT] No negotiated master services agreement found for vendor ID: '{vendor_id}'.")]
    raise ValueError(f"Unknown tool: {name}")

app = FastAPI(title="Contract Database MCP Server")
sse_transport = SseServerTransport("/messages")

@app.get("/sse")
async def handle_sse(request: Request):
    async with sse_transport.connect_scope(request.scope, request.receive, request.send):
        await server.run(
            sse_transport.read_stream,
            sse_transport.write_stream,
            server.create_initialization_options()
        )

@app.post("/messages")
async def handle_messages(request: Request):
    await sse_transport.handle_post_request(request.scope, request.receive, request.send)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
