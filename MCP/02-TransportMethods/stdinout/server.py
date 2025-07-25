from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Demo MCP Server")

@mcp.tool(description="Add two integers")
def add(a:int, b:int) -> int:
    """Add two integers."""
    return a + b

if __name__ == "__main__":
    mcp.run(transport="stdio")
