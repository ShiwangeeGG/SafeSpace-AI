import json
import chromadb
import ollama


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

    if not text or not text.strip():
        print(f"⚠️ Skipping empty chunk {i}")
        print("Source:", chunk["source"])
        continue

    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    if not response.get("embeddings"):
        print(f"⚠️ No embedding returned for chunk {i}")
        print("Source:", chunk["source"])
        print("First 200 chars:", text[:200])
        continue

    embedding = response["embeddings"][0]

    try:
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[
               {
                  "source": chunk["source"],
                  "layer": chunk["layer"],
                  "chunk_id": i,
                  "length": len(text),
                  "category": chunk["source"].split("/")[2],
                }
            ]
        )

        print(f"✅ Added chunk {i+1}")

    except Exception as e:
        print(f"❌ Error adding chunk {i+1}")
        print(e)
        break

from pathlib import Path

print("Current working directory:", Path.cwd())
print("Vector DB path:", Path("./vector_db").resolve())

print("Finished")
print("Collection contains:", collection.count(), "records")