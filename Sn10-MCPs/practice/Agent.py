import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")


class Agent:
    def __init__(self, system_prompt: str, prompt_template: str, input_key: str = "query"):
        self.llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, api_key=OPENAI_API_KEY)
        self.history: list = [SystemMessage(content=system_prompt)]
        self.template = prompt_template
        self.input_key = input_key

    def _format(self, query: str, **kwargs) -> str:
        return self.template.format(**{self.input_key: query, **kwargs})

    def chat(self, query: str, **kwargs) -> str:
        self.history.append(HumanMessage(content=self._format(query, **kwargs)))
        response = self.llm.invoke(self.history)
        self.history.append(response)
        return response.content

    def stream_chat(self, query: str, **kwargs):
        self.history.append(HumanMessage(content=self._format(query, **kwargs)))
        full = ""
        for chunk in self.llm.stream(self.history):
            full += chunk.content
            yield chunk.content
        self.history.append(AIMessage(content=full))

    def clear(self):
        self.history = [self.history[0]]
