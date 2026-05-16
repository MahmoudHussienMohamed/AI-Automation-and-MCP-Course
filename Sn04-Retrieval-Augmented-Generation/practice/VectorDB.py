import numpy as np
from Record import Record
# from EmbeddingModel import EmbeddingModel

class VectorDB:
    """Vector database with metadata filtering and cosine similarity search."""
    
    def __init__(self):
        self.records: list[Record] = []

    def add(self, text: str, embedding: np.ndarray, metadata: dict = None) -> None:
        """Add a record to the database."""
        record = Record(
            text=text,
            embedding=embedding,
            metadata=metadata or {}
        )
        self.records.append(record)

    def __len__(self) -> int:
        return len(self.records)

    def filter(self, metadata_filter: dict) -> list[Record]:
        """Filter records by metadata key-value pairs.
        
        All filter conditions must match (AND logic).
        Example: {"department": "hr", "year": 2024}
        """
        if not metadata_filter:
            return self.records
        
        return [
            record for record in self.records
            if all(record.metadata.get(k) == v for k, v in metadata_filter.items())
        ]

    def query(self, query_embedding: np.ndarray, n_results: int = 3, metadata_filter: dict = None) -> list[str]:
        """Find top-k similar texts using cosine similarity.
        
        Args:
            query_embedding: Query vector
            n_results: Number of results to return
            metadata_filter: Optional metadata constraints
            
        Returns:
            List of top-k matching text chunks
        """
        # Filter records by metadata
        filtered_records = self.filter(metadata_filter)
        if not filtered_records:
            return []

        # Stack embeddings from filtered records into matrix
        embeddings_matrix = np.stack([r.embedding for r in filtered_records])

        # Normalize query and embeddings for cosine similarity
        q_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-10) # A
        e_norms: np.ndarray = embeddings_matrix / (
            np.linalg.norm(embeddings_matrix, axis=1, keepdims=True) + 1e-10
        ) # Bs

        # Compute cosine similarities via dot product = (A · B) / (|A| * |B|)
        # scores = e_norms @ q_norm
        scores = e_norms.dot(q_norm)

        # Retrieve top results
        top_indices = np.argsort(scores)[::-1][:n_results]
        return [filtered_records[i].text for i in top_indices]

# model = EmbeddingModel()

# text1 = "My age is 26"
# t1_embeddings = model.embed(text1)

# text2 = "I'm from Egypt living there for almost 26 years"
# t2_embeddings = model.embed(text2)

# text3 = "I love travelling to Meccah"
# t3_embeddings = model.embed(text3)

# text4 = "I love travelling to Cairo"
# t4_embeddings = model.embed(text4)

# db = VectorDB()
# db.add(text1, t1_embeddings)
# db.add(text2, t2_embeddings)
# db.add(text3, t3_embeddings)
# db.add(text4, t4_embeddings)

# while True:
#     query = input("Your Query: ")
#     q_embeddings = model.embed(query)
#     print(db.query(q_embeddings, 2))
