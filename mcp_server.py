from mcp.server.fastmcp import FastMCP

# Initialize the official FastMCP server
mcp = FastMCP("Contract-Database")

# Mock Enterprise Contract Database Repository
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

@mcp.tool()
def verify_contract_terms(vendor_id: str) -> str:
    """Queries the secure contract database to retrieve baseline pricing caps."""
    vendor_id = vendor_id.lower()
    if vendor_id in MOCK_CONTRACT_REGISTRY:
        return f"[MATCH FOUND] Contract Parameters: {MOCK_CONTRACT_REGISTRY[vendor_id]}"
    return f"[ALERT] No negotiated master services agreement found for vendor ID: '{vendor_id}'."

if __name__ == "__main__":
    # Starts the MCP server natively on http://127.0.0.1:8000/sse
    mcp.run(transport="sse")