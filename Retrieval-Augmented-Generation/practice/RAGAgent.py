from OpenAIAgent import OpenAIAgent
from TextSplitter import TextSplitter
from EmbeddingModel import EmbeddingModel
from VectorDB import VectorDB

class RAGAgent(OpenAIAgent):

    def __init__(self, system_prompt: str, prompt_template: str,
                 user_input_param_name: str = "query"):
        super().__init__(system_prompt, prompt_template, user_input_param_name)
        self.embedder = EmbeddingModel()
        self.vec_db = VectorDB()
        self.splitter = TextSplitter(chunk_size=512, overlap=50)

    # ── Slide 5: Pillar 1 — Ingestion ────────────────────────────────────────
    # Loads raw text, chunks it, embeds each chunk, stores in VectorDB.
    def ingest(self, document_text: str, metadata: dict = None):
        chunks = self.splitter.split(document_text)
        for chunk in chunks:
            embedding = self.embedder.embed(chunk)
            self.vec_db.add(chunk, embedding, metadata)
        print(f"[OK] Ingested {len(chunks)} chunk(s).  "
              f"Total in DB: {len(self.vec_db)}")

    # ── Slide 8: Pillar 2 — Retrieval ────────────────────────────────────────
    # Vectorises the query and fetches the nearest document chunks.
    def retrieve(self, query: str, n_results: int = 3,
                 metadata_filter: dict = None) -> str:
        if len(self.vec_db) == 0:
            return "<context>\n(no documents ingested yet)\n</context>"

        query_embedding = self.embedder.embed(query)

        # Slide 12: (simplified) Re-ranking — cosine scores already act as a
        # quality signal; we take only the absolute best n_results chunks.
        top_chunks = self.vec_db.query(
            query_embedding,
            n_results=n_results,
            metadata_filter=metadata_filter
        )

        # Slide 9: Structural Delimiter — wrap chunks in <context> XML tags
        # so the LLM clearly understands what is injected data vs. instructions.
        context_body = "\n---\n".join(top_chunks)
        return f"<context>\n{context_body}\n</context>"

    # ── Slide 9: Pillar 3 — Augment prompt with retrieved context ────────────
    def _format_with_context(self, query: str, context: str) -> str:
        return self.prompt.format(**{self.param_name: query, "context": context})

    # ── Full RAG pipeline ─────────────────────────────────────────────────────
    def rag_chat(self, query: str, stream: bool = True,
                 metadata_filter: dict = None):
        # Store the raw user query in conversation history
        self.save_user_message(query)

        # 1. Retrieve
        context = self.retrieve(query, metadata_filter=metadata_filter)
        # print(f'\n\n\n{context}\n\n\n')


        # 2. Augment
        formatted = self._format_with_context(query, context)

        # 3. Generate
        if stream:
            return self._stream(formatted)
        return self._respond(formatted)

    def _stream(self, formatted_prompt: str):
        payload = self.request_payload(formatted_prompt, stream=True)
        full_response = ""
        for chunk in self.request_model(payload):
            content = chunk.choices[0].delta.content
            if content:
                full_response += content
                yield content
        self.save_model_message(full_response)

    def _respond(self, formatted_prompt: str) -> str:
        payload = self.request_payload(formatted_prompt, stream=False)
        response = self.request_model(payload)
        text = response.choices[0].message.content
        self.save_model_message(text)
        return text
