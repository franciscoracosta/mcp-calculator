from fastmcp import FastMCP
from middleware import SubscriptionMiddleware
import uvicorn
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Calculator Server")

# Public tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Public endpoint: Add two numbers"""
    return a + b

# Premium tool (subscription needed)
@mcp.tool(middleware=[SubscriptionMiddleware()])
def premium_multiply(a: int, b: int) -> int:
    """Premium endpoint: Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    uvicorn.run(mcp.app, host="0.0.0.0", port=8000)
