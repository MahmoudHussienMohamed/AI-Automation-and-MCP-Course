from OpenAIAgent import OpenAIAgent

# ---------------------------------------------------------
# Level 1: The Strict Classifier (Single Agent)
# ---------------------------------------------------------
# Goal: Write a system prompt that turns the LLM into a rigid intent classifier for a regional business portal.
# Categories: BUSINESS_SERVICE, GENERAL_INQUIRY, UNKNOWN.
# Constraint: Output ONLY the category name. No explanations.
# ---------------------------------------------------------

query = "I need to renew my commercial license."

# TODO: Define your system prompt here
system_prompt = """
"""

# TODO: Define your template prompt here (use {query} placeholder)
template_prompt = """
{query}
"""

# Construct the agent by passing the prompts
bot = OpenAIAgent(system_prompt, template_prompt)

print(f"Query: {query}")
print("Classification:", end=" ")

# Call the agent
response = bot.nonstream_chat(query)
print(response) # Expected output: BUSINESS_SERVICE

# Feel free to test with other inputs!