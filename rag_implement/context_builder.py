#context_builder.py
# remove_duplicates()
# format_document()
# build_context()
# preview_context()

# removal of duplicates 
def remove_duplicates(results):

    seen = set()

    unique_docs = []

    unique_meta = []

    unique_distance = []

    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        if doc not in seen:

            seen.add(doc)

            unique_docs.append(doc)

            unique_meta.append(meta)

            unique_distance.append(distance)

    return unique_docs, unique_meta, unique_distance

#converting raw chunk into format 
def format_document(index,
                    document,
                    metadata,
                    distance):

    return f"""
==================================================
DOCUMENT {index}

Source:
{metadata["source"]}

Layer:
{metadata["layer"]}

Similarity Distance:
{distance:.2f}

Content:

{document}

"""

#merging everthing 
def build_context(question,
                  results):

    docs, metas, distances = remove_duplicates(results)

    context = []

    context.append(
f"""
==========================================

SAFE SPACE AI KNOWLEDGE CONTEXT

==========================================

User Question

{question}

Retrieved Documents

{len(docs)}

==========================================

"""
    )

    for i, (doc, meta, distance) in enumerate(

        zip(
            docs,
            metas,
            distances
        ),

        start=1

    ):

        context.append(

            format_document(

                i,
                doc,
                meta,
                distance

            )

        )

    context.append(

        "\n========== END OF CONTEXT ==========\n"

    )

    return "\n".join(context)

#debugging
def preview_context(context):

    print(context)

if __name__ == "__main__":
    print("Context Builder Loaded Successfully!")    