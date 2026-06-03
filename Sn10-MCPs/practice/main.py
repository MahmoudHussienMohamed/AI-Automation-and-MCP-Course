import os
import asyncio
from ExecuterAgent import ExecutorAgent


SERVER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "tools.py"
)

config = {
    "utilities": {
        "command": "python",
        "args": [SERVER_PATH],
        "transport": "stdio",
    }
}

executor = ExecutorAgent(
    system_prompt="You are an agent with access to tools.",
    prompt_template="{query}",
    mcp_config=config
)

async def main():
    query = input("Your Query: ")
    response = await executor.execute(query)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())
