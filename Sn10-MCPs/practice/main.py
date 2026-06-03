import os
import asyncio
from ExecuterAgent import ExecutorAgent


SERVERS_DIR = os.path.dirname(os.path.abspath(__file__))

TOOLS_PATH = os.path.join(SERVERS_DIR, "tools.py")
NOTES_PATH = os.path.join(SERVERS_DIR, "notes.py")

config = {
    "utilities": {
        "command": "python",
        "args": [TOOLS_PATH],
        "transport": "stdio",
    },
    "notes": {
        "command": "python",
        "args": [NOTES_PATH],
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
