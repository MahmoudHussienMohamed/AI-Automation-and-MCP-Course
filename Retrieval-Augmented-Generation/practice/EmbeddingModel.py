import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

class EmbeddingModel:
    def __init__(self, model: str = OPENAI_EMBEDDING_MODEL):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def embed(self, text: str):
        response = self.client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=text
        )
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        return embedding
