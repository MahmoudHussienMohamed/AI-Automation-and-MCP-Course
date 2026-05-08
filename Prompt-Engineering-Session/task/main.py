from src.OpenAIAgent import OpenAIAgent

template = """
Answer to the user given the following data:
sdlkjfhskdfjh
sdikfgsfg
iksdgfsijdfg
user query:
{query}
## instructions:
    - 
    -
    -
"""

agent = OpenAIAgent(
    system_prompt="You're a helpful assistant in business.",
    prompt_template=template
)

agent.nonstream_chat(query="")