import chromadb

from services.embedding_service import generate_embedding
from services.knowledge_repository import get_documents


# -----------------------------
# ChromaDB Configuration
# -----------------------------
client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_or_create_collection(
    name="governance_knowledge"
)


# -----------------------------
# Index Documents
# -----------------------------
def index_documents():

    documents = get_documents()

    for document in documents:

        document_name = document["name"].replace(".json", "")
        data = document["data"]

        for category, entities in data.items():

            for entity in entities:

                # -----------------------------
                # Category-specific context
                # -----------------------------
                if category == "roles":
                    intro = (
                        "This entity represents an AI governance role. "
                        "It defines responsibilities, ownership, accountability, "
                        "or duties related to AI systems."
                    )

                elif category == "controls":
                    intro = (
                        "This entity represents an AI governance control. "
                        "It describes organizational measures, safeguards, "
                        "or practices used to govern AI systems."
                    )

                elif category == "ethical_principles":
                    intro = (
                        "This entity represents an AI ethics principle. "
                        "It defines values and concepts that guide "
                        "responsible AI development and use."
                    )

                elif category == "risks":
                    intro = (
                        "This entity represents an AI risk. "
                        "It describes potential threats, impacts, or concerns "
                        "associated with AI systems."
                    )

                elif category == "policies":
                    intro = (
                        "This entity represents an AI governance policy. "
                        "It describes organizational rules or requirements "
                        "for managing AI."
                    )

                else:
                    intro = (
                        f"This entity belongs to the AI governance category "
                        f"'{category}'."
                    )

                # -----------------------------
                # Text used for embeddings
                # -----------------------------
                text = f"""
{intro}

Document:
{document_name}

Category:
{category}

Entity:
{entity["name"]}

Description:
{entity["description"]}

Source:
{entity["source_text"]}
"""

                embedding = generate_embedding(text)

                entity_id = (
                    f"{document_name}_{category}_{entity['name']}"
                    .lower()
                    .replace(" ", "_")
                )

                collection.add(
                    ids=[entity_id],
                    embeddings=[embedding],
                    documents=[text],
                    metadatas=[
                        {
                            "document": document_name,
                            "category": category,
                            "name": entity["name"],
                            "description": entity["description"],
                            "source_text": entity["source_text"],
                        }
                    ],
                )

    print("✅ Knowledge indexed successfully.")


# -----------------------------
# Semantic Search
# -----------------------------
def semantic_search(query, n_results=5):

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    search_results = []

    for i in range(len(results["metadatas"][0])):

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        result = {
            "name": metadata["name"],
            "category": metadata["category"],
            "document": metadata["document"],
            "description": metadata["description"],
            "source_text": metadata["source_text"],
            "distance": distance,
        }

        search_results.append(result)

    return search_results


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":

    index_documents()

    print(
        semantic_search(
            "Who is responsible for AI governance?"
        )
    )