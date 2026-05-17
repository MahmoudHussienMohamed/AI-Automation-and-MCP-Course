from Agent import Agent
from RAGAgent import RAGAgent
from ExecuterAgent import ExecutorAgent
from tools import TOOLS


# agent = Agent(
#     system_prompt="You are a helpful assistant.",
#     prompt_template="Answer this: {query}",
# )

# query = input("Your Query: ")
# print(agent.chat(query))

# query = input("Your Query: ")
# for chunk in agent.stream_chat("Explain LCEL briefly"):
#     print(chunk, end="", flush=True)


# rag = RAGAgent(
#     system_prompt="Answer only from the provided context.",
#     prompt_template="Context: {context}\n\nQuestion: {query}",
# )

# rag.ingest("محمود حسين محمد مهندس ذكاء اصطناعي.")
# rag.ingest("محمود شغال في شركة مزيد أي تي.")
# query = input("Your Query: ")
# print(rag.rag_chat(query))

query = input("Your Query: ")
# ExecutorAgent
executor = ExecutorAgent(
    system_prompt="You are an agent with access to tools.",
    prompt_template="{query}",
    tools=TOOLS,
)
print(executor.execute(query))
