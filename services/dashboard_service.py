from services.knowledge_repository import get_documents
from services.knowledge_explorer import get_all_entities


def get_dashboard_data():
    """
    Collect all information required by the Dashboard.
    """

    # ---------------------------------------------
    # Documents
    # ---------------------------------------------

    documents = get_documents()

    total_documents = len(documents)

    recent_documents = [
        document["name"]
        for document in documents[-5:]
    ]

    # ---------------------------------------------
    # Knowledge
    # ---------------------------------------------

    knowledge = get_all_entities()

    total_categories = len(knowledge)

    total_entities = sum(
        len(entities)
        for entities in knowledge.values()
    )

    # ---------------------------------------------
    # Category Statistics
    # ---------------------------------------------

    category_distribution = {
        category.replace("_", " ").title(): len(entities)
        for category, entities in knowledge.items()
    }

    # Sort from largest to smallest

    category_distribution = dict(
        sorted(
            category_distribution.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    # ---------------------------------------------
    # Dashboard Object
    # ---------------------------------------------

    return {
        "total_documents": total_documents,
        "total_entities": total_entities,
        "total_categories": total_categories,
        "category_distribution": category_distribution,
        "recent_documents": recent_documents,
    }