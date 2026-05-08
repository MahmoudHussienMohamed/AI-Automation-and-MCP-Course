from RAGAgent import RAGAgent
import json
        # "If the answer is not contained in the context, respond with exactly: DATA_NOT_FOUND"
if __name__ == "__main__":

    # ── Slide 10: Enforcing Deterministic Outputs ─────────────────────────────
    SYSTEM_PROMPT = (
        "You are a corporate policy assistant. "
        "Answer the user's query using ONLY the data provided inside the <context> block. "
        "If the answer is not relevant in the context, respond with exactly: DATA_NOT_FOUND"
    )

    # The prompt template MUST expose both {query} and {context} placeholders.
    PROMPT_TEMPLATE = (
        "Context Information:\n{context}\n\n"
        "Employee Question: {query}\n\n"
        "provide your confidence score and the reason that makes you responde like that"
        "Answer (based strictly on the context above):"
    )

    agent = RAGAgent(
        system_prompt=SYSTEM_PROMPT,
        prompt_template=PROMPT_TEMPLATE
    )

    # ── Pillar 1: Ingestion Phase ─────────────────────────────────────────────
    print("=== INGESTION PHASE ===\n")

    try:
        with open("synthetic_policies.json", "r") as f:
            policies = json.load(f)
        for policy in policies:
            agent.ingest(policy["text"], metadata=policy["metadata"])
    except FileNotFoundError:
        print("synthetic_policies.json not found, falling back to manual ingestion.")
        agent.ingest(
            "Our refund policy allows returns within 30 days of purchase. "
            "Items must be in original packaging with a receipt.",
            metadata={"department": "sales", "year": 2024}
        )
        agent.ingest(
            "Remote work policy (2022): employees may work remotely up to 10 days per year.",
            metadata={"department": "hr", "year": 2022}
        )
        agent.ingest(
            "Remote work policy (2024): employees may work fully remotely. "
            "Prior approval from direct manager is required.",
            metadata={"department": "hr", "year": 2024}
        )

    # ── Pillars 2 & 3: Retrieval + Generation (interactive chat) ─────────────
    print("\n=== CHAT PHASE ===")
    print("Ask anything about company policies. Type 'exit' to quit.\n")

    while True:
        query = input("Employee: ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break

        print("Assistant: ", end="", flush=True)

        # Slide 11: Metadata filter — only search the 2024 policy documents
        for token in agent.rag_chat(query, stream=True, metadata_filter={"year": 2024}):
            print(token, end="", flush=True)

        print("\n")
