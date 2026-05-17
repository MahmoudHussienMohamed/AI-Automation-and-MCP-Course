from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from Agent import Agent


class RAGAgent(Agent):
    def __init__(self, system_prompt: str, prompt_template: str, input_key: str = "query"):
        super().__init__(system_prompt, prompt_template, input_key)
        self.embeddings = OpenAIEmbeddings()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        self.vectorstore: FAISS | None = None

    def ingest(self, text: str, metadata: dict = None):
        docs = self.splitter.create_documents([text], metadatas=[metadata or {}])
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(docs, self.embeddings)
        else:
            self.vectorstore.add_documents(docs)
        print(f"[OK] Ingested {len(docs)} chunk(s). Total: {self.vectorstore.index.ntotal}")

    def retrieve(self, query: str, k: int = 3, filter: dict = None) -> str:
        if not self.vectorstore:
            return "<context>\n(no documents ingested yet)\n</context>"
        docs = self.vectorstore.similarity_search(query, k=k, filter=filter)
        body = "\n---\n".join(d.page_content for d in docs)
        return f"<context>\n{body}\n</context>"

    def rag_chat(self, query: str, stream: bool = False, filter: dict = None):
        context = self.retrieve(query, filter=filter)
        if stream:
            return self.stream_chat(query, context=context)
        return self.chat(query, context=context)
