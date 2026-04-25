from OpenAIAgent import OpenAIAgent
import json

# ---------------------------------------------------------
# Level 2: The Structured Extractor (Single Agent, Strict Format)
# ---------------------------------------------------------
# Goal: Extract specific information from a noisy text and format it strictly as JSON.
# Entities to extract: `Company Name`, `Filing Date`, and `Status` (Active/Inactive).
# Constraint: Missing values must be `null`. Output must be raw valid JSON (no markdown wrapping).
# ---------------------------------------------------------

query = "Um, yeah, we registered Apex Dynamics on... I think it was March 14th, 2023. We are currently fully operational."

# TODO: Define your system prompt here
system_prompt = """
"""

# TODO: Define your template prompt here (use {query} placeholder)
template_prompt = """
{query}
"""

# Construct the agent by passing the prompts
bot = OpenAIAgent(system_prompt, template_prompt)

print("Extracting...")
response = bot.nonstream_chat(query)

print("Raw Response:")
print(response)

# The response should be parsable directly into a Python dictionary
try:
    data = json.loads(response)
    print("\nSuccessfully parsed JSON:")
    print(json.dumps(data, indent=2))
except json.JSONDecodeError as e:
    print(f"\nFailed to parse JSON. Error: {e}")
    print("Make sure your prompt forces the LLM to output ONLY raw JSON without markdown formatting like ```json")