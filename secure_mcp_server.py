import sys
from mcp.server.fastmcp import FastMCP
from AuthSec_SDK import protected_by_AuthSec, run_mcp_server_with_oauth

# IMPORTANT: log only to stderr
print("Secure BMI MCP Server starting...", file=sys.stderr)

mcp = FastMCP("Secure BMI MCP Server")

@protected_by_AuthSec("bmi.calculate")
@mcp.tool()
def calculate_bmi(weight: float, height_cm: float, user_info=None) -> dict:
    # Verify user has permission to use the calculator
    if not user_info:
        return {
            "error": "Access denied",
            "message": "Authentication required. Please log in to use the BMI calculator."
        }
    
    if not user_info.get("email"):
        return {
            "error": "Invalid user",
            "message": "Valid user email required to access this service."
        }
    
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
        calorie_adjustment = 300
    elif bmi < 25:
        category = "Normal"
        calorie_adjustment = 0
    elif bmi < 30:
        category = "Overweight"
        calorie_adjustment = -300
    else:
        category = "Obese"
        calorie_adjustment = -500

    base_calories = weight * 30
    recommended_calories = int(base_calories + calorie_adjustment)

    return {
        "user": user_info.get("email") if user_info else None,
        "bmi": bmi,
        "category": category,
        "recommended_calories": recommended_calories
    }

if __name__ == "__main__":
    run_mcp_server_with_oauth(
        user_module=sys.modules[__name__],
        client_id="40cbd672-3289-42be-9840-cf492d81769c",
        app_name="Secure BMI MCP Server",
        host="0.0.0.0",
        port=3005
    )