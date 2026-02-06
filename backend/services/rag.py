def retrieve_top_chunks(search_client, query_vector, doc_id: str, k: int = 5):
    results = search_client.search(
        search_text="",
        vector_queries=[{
            "vector": query_vector,
            "k_nearest_neighbors": k,
            "fields": "contentVector"
        }],
        filter=f"doc_id eq '{doc_id}'",
        select=["content", "chunk_index", "filename", "doc_id"]
    )
    chunks = []
    for r in results:
        chunks.append(r["content"])
    return chunks

def build_prompt(question: str, chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(chunks)
    return f"""Use the provided context to answer the question.
If the answer is not in the context, say: "I couldn't find that in the document."

Context:
{context}

Question:
{question}

Answer:"""
