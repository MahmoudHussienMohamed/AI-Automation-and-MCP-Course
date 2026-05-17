from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from Agent import Agent


class ExecutorAgent(Agent):
    def __init__(self, system_prompt: str, prompt_template: str, tools: list[BaseTool], input_key: str = "query"):
        super().__init__(system_prompt, prompt_template, input_key)
        self.tools = {t.name: t for t in tools}
        self.llm = self.llm.bind_tools(tools)

    def execute(self, query: str) -> str:
        self.history.append(HumanMessage(content=self._format(query)))
        response = self.llm.invoke(self.history)
        self.history.append(response)

        while response.tool_calls:
            for tc in response.tool_calls:
                name = tc["name"]
                args = tc["args"]
                print(f'Executing tool `{name}({args})`')
                result = self.tools[name].invoke(args)
                print(f'\tResult: "{result}"')
                self.history.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
            response = self.llm.invoke(self.history)
            self.history.append(response)

        return response.content
