from services.vector_store import semantic_search
from services.llm_service import ask_llm


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MAX_RESULTS = 5

# Lower distance = better match (Chroma uses distance)
MAX_DISTANCE = 1.15


# --------------------------------------------------
# Build Context
# --------------------------------------------------

def build_context(search_results):
    """
    Build a readable context for the LLM.
    """

    sections = []

    for i, result in enumerate(search_results, start=1):

        sections.append(
            f"""
==============================
Knowledge {i}

Document:
{result["document"]}

Category:
{result["category"]}

Entity:
{result["name"]}

Description:
{result["description"]}

Source:
{result["source_text"]}
"""
        )

    return "\n".join(sections)


# --------------------------------------------------
# RAG Pipeline
# --------------------------------------------------

def ask_knowledge_base(question):

    # ------------------------------------------
    # Retrieve relevant knowledge
    # ------------------------------------------

    search_results = semantic_search(
        question,
        n_results=MAX_RESULTS
    )

    # ------------------------------------------
    # Filter weak matches
    # ------------------------------------------

    relevant_results = [
        result
        for result in search_results
        if result["distance"] <= MAX_DISTANCE
    ]

    if not relevant_results:

        return {
            "answer": (
                "I couldn't find relevant information in the "
                "knowledge base to answer your question."
            ),
            "sources": []
        }

    # ------------------------------------------
    # Build context
    # ------------------------------------------

    context = build_context(relevant_results)

    # ------------------------------------------
    # System Prompt
    # ------------------------------------------

    system_prompt = """
You are an AI Governance Assistant specialized in ISO/IEC 42001.

Your task is to answer questions ONLY using the provided knowledge.

Instructions:

- Never use external knowledge.
- Never invent information.
- If the context is insufficient, explicitly say so.
- Combine multiple knowledge entries when appropriate.
- Write clear and professional answers.
- Use bullet points whenever they improve readability.
- Keep answers concise but complete.
- Mention important roles, controls, risks or principles when relevant.
"""

    # ------------------------------------------
    # User Prompt
    # ------------------------------------------

    user_prompt = f"""
Knowledge Base

{context}

------------------------------------------------------------

User Question

{question}

------------------------------------------------------------

Answer:
"""

    # ------------------------------------------
    # Generate answer
    # ------------------------------------------

    answer = ask_llm(
        system_prompt,
        user_prompt
    )

    # ------------------------------------------
    # Return answer + sources
    # ------------------------------------------

    return {
        "answer": answer,
        "sources": relevant_results
    }