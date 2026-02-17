import sys
from mcp.server.fastmcp import FastMCP

# IMPORTANT: stderr only (never stdout)
print("BMI MCP Server starting...", file=sys.stderr)

mcp = FastMCP("BMI MCP Server")

@mcp.tool()
def calculate_bmi(weight: float, height_cm: float) -> dict:
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        "bmi": bmi,
        "category": category
    }

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception as e:
        print("MCP crashed:", e, file=sys.stderr)
        raise