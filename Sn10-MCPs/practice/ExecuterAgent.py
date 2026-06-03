import asyncio
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from Agent import Agent


class ExecutorAgent(Agent):
    def __init__(self, system_prompt: str, prompt_template: str, mcp_config: dict, input_key: str = "query"):
        super().__init__(system_prompt, prompt_template, input_key)
        self.mcp_config = mcp_config

    async def execute(self, query: str) -> str:
        mcp = MultiServerMCPClient(self.mcp_config)
        tools = await mcp.get_tools()
        llm = self.llm.bind_tools(tools)
        tool_map = {t.name: t for t in tools}

        self.history.append(HumanMessage(content=self._format(query)))
        response = await llm.ainvoke(self.history)
        self.history.append(response)

        while response.tool_calls:
            for tool_call in response.tool_calls:
                name, args = tool_call["name"], tool_call["args"]
                print(f'Executing tool `{name}({args})`')
                result = await tool_map[name].ainvoke(args)
                print(f'\tResult: "{result}"')
                self.history.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
            response = await llm.ainvoke(self.history)
            self.history.append(response)

        return response.content