import json

from ExecuterAgent import ExecuterAgent
from tool_decorator import TOOLS_REGISTRY
from tools import add_numbers
agent = ExecuterAgent(
    system_prompt="You are a helpful assistant that solves problems.",
    prompt_template="Answer the following user query *ONLY* using provided tools: \"\"\"{query}\"\"\"",
)

query = input("Your query: ")

print(agent.execute(query))

# function = TOOLS_REGISTRY['multiply_numbers']['function']
# args = '{"a": 5, "b": 3}'
# print(f'OpenAI Resoponse: {args}')
# args = json.loads(args)
# print(f'After json loading: {args}')
# print(f'function output: {add_numbers(**args)}')
# print(f'function output: {add_numbers(a=args['a'], b=args['b'])}')
# print(function(5, 3))
# print(json.dumps(function, indent=2))