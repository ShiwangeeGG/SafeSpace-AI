print("STARTING RETRIEVER...")

import chromadb
from ollama import embeddings

client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_collection(
    name="safespace_ai"
)

query = input("Ask SafeSpace AI: ")

query_embedding = embeddings(
    model="nomic-embed-text",
    prompt=query
)["embedding"]

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=7
)

for doc, meta, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):

    print("=" * 60)
    print("SOURCE :", meta["source"])
    print("LAYER  :", meta["layer"])
    #print(f"DISTANCE : {distance:.2f}")
    print("=" * 60)

    print(doc)
    print()

print("DONE")