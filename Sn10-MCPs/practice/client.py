import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'servers')

SERVER_PATH = os.path.join(SERVERS_DIR, "tools.py")

print(SERVER_PATH)

config = {
    "utilities": {
        "command": "python",
        "args": [SERVER_PATH],
        "transport": "stdio",
    }
}

async def main():
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()

    tool_map = {
        tool.name: tool
        for tool in tools
    }
    
    print(tool_map.keys(), '\n')
    
    result = await tool_map['get_current_time'].ainvoke({})
    print(result)
    
    result = await tool_map['add_numbers'].ainvoke({'a': 5, 'b': 3})
    print(result)


if __name__ == '__main__':
    asyncio.run(main())