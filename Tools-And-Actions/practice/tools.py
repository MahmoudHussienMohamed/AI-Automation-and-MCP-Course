import json

from tool_decorator import *

@openai_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers.
    a: First number
    b: Second number
    """
    return a + b


@openai_tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers.
    a: First number
    b: Second number
    """
    return a * b

@openai_tool
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers.
    a: First number
    b: Second number
    """
    return a / b


@openai_tool
def get_current_time() -> str:
    """Get the current date and time in ISO format.
    """
    from datetime import datetime
    return datetime.now().isoformat()


@openai_tool
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information.
    query: Search query
    """
    try:
        import wikipedia
        results = wikipedia.search(query)
        if results:
            return wikipedia.summary(results[0], sentences=3)
        return f"No results found for '{query}'"
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


@openai_tool
def get_weather(city: str) -> str:
    """Get current weather for a city (mock implementation).
    city: City name
    """
    # Mock weather data
    mock_data = {
        "London": "15°C, Cloudy",
        "New York": "22°C, Sunny",
        "Tokyo": "18°C, Rainy",
        "Paris": "16°C, Partly Cloudy"
    }
    return mock_data.get(city, f"Weather data not available for {city}")


@openai_tool
def calculate_factorial(n: int) -> int:
    """Calculate factorial of a number.
    n: The number (must be non-negative)
    """
    if n < 0:
        return "Error: n must be non-negative"
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@openai_tool
def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between Celsius and Fahrenheit.
    value: Temperature value
    from_unit: Source unit ('C' or 'F')
    to_unit: Target unit ('C' or 'F')
    """
    if from_unit == to_unit:
        return value
    if from_unit == 'C' and to_unit == 'F':
        return (value * 9/5) + 32
    elif from_unit == 'F' and to_unit == 'C':
        return (value - 32) * 5/9
    return "Error: Invalid units"


# @openai_tool
# def get_word_definition(word: str) -> str:
#     """Get the definition of a word.
#     word: The word to define
#     """
#     try:
#         import urllib.request
#         import json
        
#         url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
#         with urllib.request.urlopen(url, timeout=5) as response:
#             data = json.loads(response.read())
#             if data:
#                 definition = data[0].get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', 'No definition found')
#                 return definition
#             return f"No definition found for '{word}'"
#     except Exception as e:
#         return f"Error fetching definition: {str(e)}"


@openai_tool
def list_files(directory: str = ".") -> str:
    """List files in a directory.
    directory: Path to directory (default: current directory)
    """
    import os
    try:
        files = os.listdir(directory)
        return f"Files in {directory}: {', '.join(files[:10])}"
    except Exception as e:
        return f"Error listing files: {str(e)}"


@openai_tool
def get_file_size(filepath: str) -> str:
    """Get the size of a file in bytes.
    filepath: Path to the file
    """
    import os
    try:
        size = os.path.getsize(filepath)
        return f"File size: {size} bytes ({size / 1024:.2f} KB)"
    except Exception as e:
        return f"Error getting file size: {str(e)}"


@openai_tool
def calculate_average(numbers: list) -> float:
    """Calculate the average of a list of numbers.
    numbers: List of numbers as "[a, b, ...]"
    """
    if not isinstance(numbers, list):
        numbers = json.loads(numbers)
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


@openai_tool
def text_to_uppercase(text: str) -> str:
    """Convert text to uppercase.
    text: The text to convert
    """
    return text.upper()


@openai_tool
def count_words(text: str) -> int:
    """Count the number of words in text.
    text: The text to analyze
    """
    return len(text.split())


# if __name__ == "__main__":
#     # Display all registered tools
#     print("Registered Tools:")
#     print("=" * 50)
#     for tool_name, tool_data in TOOLS_REGISTRY.items():
#         print(f"\n{tool_name}:")
#         print(json.dumps(tool_data["schema"], indent=2))

#     print(add_numbers(2, 3))
#     print(convert_temperature(100, 'C', to_unit='F'))