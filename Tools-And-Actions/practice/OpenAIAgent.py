# 1:15 am
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")


class OpenAIAgent:
    def __init__(self, system_prompt: str, prompt_template: str, user_input_param_name: str = "query"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_CHAT_MODEL
        self.prompt = prompt_template
        self.param_name = user_input_param_name
        self.history = []
        self.save_system_message(system_prompt)

    @staticmethod
    def is_valid_snapshot(snapshot: dict):
        return (
            isinstance(snapshot, dict) and
            isinstance(snapshot.get('role', None), str) and # has "role"?
            isinstance(snapshot.get('content', None), str)  # has "content"?
        )

    def save_message(self, snapshot: dict):
        if not OpenAIAgent.is_valid_snapshot(snapshot):
            raise ValueError(f'Message snapshot must be dict with {{"role": "str role...", "content": "str content..."}}, but got: ({snapshot})')
        self.history.append(snapshot)

    @staticmethod
    def message_snapshot(role: str, content: str):
        return {
            "role": role,
            "content": content
        }

    @staticmethod
    def system_snapshot(content: str):
        return OpenAIAgent.message_snapshot("system", content)

    @staticmethod
    def user_snapshot(content: str):
        return OpenAIAgent.message_snapshot("user", content)

    @staticmethod
    def model_snapshot(content: str):
        return OpenAIAgent.message_snapshot("assistant", content)

    def save_system_message(self, content: str):
        self.save_message(OpenAIAgent.system_snapshot(content))

    def save_user_message(self, content: str):
        self.save_message(OpenAIAgent.user_snapshot(content))

    def save_model_message(self, content: str):
        self.save_message(OpenAIAgent.model_snapshot(content))

    def format(self, query: str):
        formatting_dict = {
            self.param_name: query
        }
        return self.prompt.format(**formatting_dict)

    def request_model(self, payload: dict):
        return self.client.chat.completions.create(**payload)
    
    def request_payload(self, message: str, stream: bool):
        messages = self.history[:-1] + [OpenAIAgent.user_snapshot(content=message)]
        return {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

    def stream_request(self, message: str):
        payload = self.request_payload(message, stream=True)
        return self.request_model(payload)
    
    def nonstream_request(self, message: str):
        payload = self.request_payload(message, stream=False)
        return self.request_model(payload)

    def chat(self, query: str, stream: bool):
        self.save_user_message(query)
        formatted = self.format(query)
        if stream:
            return self.stream_request(formatted)
        return self.nonstream_request(formatted)

    def stream_chat(self, query: str):
        full_response_content = ""
        stream = self.chat(query, stream=True)
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                full_response_content += content
                yield content
        self.save_model_message(full_response_content)
    
    def nonstream_chat(self, query: str):
        response = self.chat(query, stream=False)
        message = response.choices[0].message
        text = message.content
        self.save_model_message(text)
        return text

    def clear_history(self):
        self.history = [self.history[0]]