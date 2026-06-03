import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("utilities")

@mcp.tool()
def add_numbers(a: float, b: float) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""
    return a / b


@mcp.tool()
def get_current_time() -> str:
    """Get the current date and time in ISO format."""
    return datetime.now().isoformat()


@mcp.tool()
def search_wikipedia(query: str) -> str:
    """Search Wikipedia and return a short summary."""
    try:
        import wikipedia
        results = wikipedia.search(query)
        if results:
            return wikipedia.summary(results[0], sentences=3)
        return f"No results found for '{query}'"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city (mock)."""
    mock = {
        "London": "15°C, Cloudy",
        "New York": "22°C, Sunny",
        "Tokyo": "18°C, Rainy",
        "Paris": "16°C, Partly Cloudy",
    }
    return mock.get(city, f"Weather data not available for {city}")


@mcp.tool()
def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@mcp.tool()
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a temperature between Celsius ('C') and Fahrenheit ('F')."""
    if from_unit == to_unit:
        return value
    if from_unit == "C" and to_unit == "F":
        return (value * 9 / 5) + 32
    if from_unit == "F" and to_unit == "C":
        return (value - 32) * 5 / 9
    raise ValueError(f"Invalid units: {from_unit} -> {to_unit}")


@mcp.tool()
def list_files(directory: str = ".") -> str:
    """List up to 10 files in a directory."""
    try:
        files = os.listdir(directory)
        return f"Files in '{directory}': {', '.join(files[:10])}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_file_size(filepath: str) -> str:
    """Get the size of a file in bytes and KB."""
    try:
        size = os.path.getsize(filepath)
        return f"{size} bytes ({size / 1024:.2f} KB)"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


@mcp.tool()
def text_to_uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words in a text string."""
    return len(text.split())


# TOOLS = [
#     add_numbers,
#     multiply_numbers,
#     divide_numbers,
#     get_current_time,
#     search_wikipedia,
#     get_weather,
#     calculate_factorial,
#     convert_temperature,
#     list_files,
#     get_file_size,
#     calculate_average,
#     text_to_uppercase,
#     count_words,
# ]

# tools = mcp._tool_manager.list_tools()
# # print(json.dumps(str(tools), indent=2))
# # tools = [tool.model_dump_json(indent=2) for tool in tools]
# tools = [tool.model_dump() for tool in tools]
# # print(json.dumps(tools, indent=2))
# print(tools)

if __name__ == '__main__':
    mcp.run()