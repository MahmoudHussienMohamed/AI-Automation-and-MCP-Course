from ExecuterAgent import ExecuterAgent
from tools import search_wikipedia

agent = ExecuterAgent(
    system_prompt="You are a helpful assistant that solves problems.",
    prompt_template="Answer the following user query *ONLY* using provided tools: \"\"\"{query}\"\"\"",
)

query = input("Your query: ")

# for chunk in agent.stream_chat(query): 
#     print(chunk, end='', flush=True)
print(agent.execute(query))