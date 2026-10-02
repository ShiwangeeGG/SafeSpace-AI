import chromadb
from ollama import embeddings

from context_builder import build_context


client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_collection(
    name="safespace_ai"
)


question = "What are fire safety requirements for hospitals?"


query_embedding = embeddings(
    model="nomic-embed-text",
    prompt=question
)["embedding"]


results = collection.query(
    query_embeddings=[query_embedding],
    n_results=7
)


context = build_context(
    question,
    results
)


print(context)