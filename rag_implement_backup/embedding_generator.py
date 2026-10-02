import json
import chromadb
from ollama import embeddings


client = chromadb.PersistentClient(
    path="./vector_db"
)

collection = client.get_or_create_collection(
    name="safespace_ai"
)


with open(
    "./chunks/all_chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)


for i, chunk in enumerate(chunks):

    text = chunk["content"]

    response = embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    embedding = response["embedding"]

    print(type(embedding))
    print(len(embedding))

    print(response)
    break

    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[
            {
                "source": chunk["source"]
            }
        ]
    )

    print(
        f"Embedded {i+1}/{len(chunks)}"
    )

print("Finished")