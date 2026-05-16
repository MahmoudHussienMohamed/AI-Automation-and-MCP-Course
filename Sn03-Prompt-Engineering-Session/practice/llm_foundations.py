import os
from typing import List, Dict, Generator
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("OPENAI_CHAT_MODEL")


class OpenAIAgent:
    def __init__(self, model: str = DEFAULT_MODEL, prompt: str = "{query}", system_prompt: str = "You are a helpful assistant."):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.prompt = prompt
        self.model = model
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]

    def stream_chat(self, user_input: str) -> Generator[str, None, None]:
        formatted = self.prompt.format(query=user_input)
        self.history.append({"role": "user", "content": formatted})
        
        full_response_content = ""
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                stream=True,
            )
            
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response_content += content
                    yield content
            
            self.history.append({"role": "assistant", "content": full_response_content})
            
        except Exception as e:
            yield f"\n[Error]: {str(e)}"

    def clear_history(self):
        """Resets the conversation while keeping the system prompt."""
        self.history = [self.history[0]]
        print("\n--- Conversation History Cleared ---")


template = """
don't answer the user any questions outside your scope (which is technical helping).

user question: {input}
"""

if __name__ == "__main__":
#     template = """
# ## Ins:
#     ### Dos
#         - don't answer the user any questions outside your scope (which is cooking helping).
#     ### Don'ts
#         - drift the conversation only to your scope after showing empathy to user if he has issue.

# ## Tone:
#     - showing empathy
#     - giving 


# user question: {query}
# """
    template = """
you will get user's feedback about our products, classify his feelings.
<instructions>
- answer only with json object reflecting the feelings of user as:
    {{"class": <feelings>}}
<\instructions>
user feedback: {query}
"""
    # bot = OpenAIAgent(system_prompt="You are a witty cooking mentor. Keep advice concise.", prompt=template)
    bot = OpenAIAgent(prompt=template)

    
    while True:
        user_query = input("\n🧔: ")
        print(template.format(query=user_query))
        if user_query.lower() in ["exit", "quit"]:
            break
        print("🤖: ", end="", flush=True)
        for chunk in bot.stream_chat(user_query):
            print(chunk, end="", flush=True)

        print()
# TEMPLATE = """
# You're technical support engineer in software company. Help user with his inquiry.
# user inquiry: {query}
# """
# print(TEMPLATE.format(query="Hi there!"))