from OpenAIAgent import OpenAIAgent

# ---------------------------------------------------------
# Level 3: The Advisory Pipeline (Multi-Agent)
# ---------------------------------------------------------
# Goal: Build a pipeline where Agent A's output serves as input for Agent B.
#
# Agent A (The Analyst): Reads user problem -> Outputs ONLY a bulleted list of core legal/business requirements.
# Agent B (The Advisor): Reads Agent A's bulleted list -> Drafts a polite, formal, and empathetic email.
# ---------------------------------------------------------

query = "I want to open a branch of my tech startup in the new administrative zone, but I don't know what permits I need for foreign workers."

# TODO: Define your system prompt for Agent A
analyst_system_prompt = """
"""

# TODO: Define Agent A's template prompt (use {query} placeholder)
analyst_template_prompt = """
{query}
"""

agent_a = OpenAIAgent(analyst_system_prompt, analyst_template_prompt)

# TODO: Define your system prompt for Agent B
advisor_system_prompt = """
"""

# TODO: Define Agent B's template prompt (use {query} placeholder)
advisor_template_prompt = """
{query}
"""

agent_b = OpenAIAgent(advisor_system_prompt, advisor_template_prompt)

# --- 1. Call Agent A (The Analyst) ---
print("--- Agent A: Analyzing Requirements ---")
requirements_list = agent_a.nonstream_chat(query)
print(requirements_list)
print("\n" + "="*50 + "\n")

# --- 2. Call Agent B (The Advisor) using Agent A's output ---
print("--- Agent B: Drafting Response ---")
# We pass requirements_list as the query to Agent B
for chunk in agent_b.stream_chat(requirements_list):
    print(chunk, end="", flush=True)
print() # Final newline