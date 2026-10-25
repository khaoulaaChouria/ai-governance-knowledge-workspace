import json
import os

# Folder where extracted knowledge is stored
KNOWLEDGE_FOLDER = "knowledge"


def get_documents():
    """
    Returns all knowledge documents stored as JSON files.

    Returns:
        list: A list of dictionaries containing:
            - name
            - path
            - data
    """

    documents = []

    if not os.path.exists(KNOWLEDGE_FOLDER):
        return documents

    for filename in sorted(os.listdir(KNOWLEDGE_FOLDER)):

        if filename.endswith(".json"):

            path = os.path.join(KNOWLEDGE_FOLDER, filename)

            try:
                with open(path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                documents.append({
                    "name": filename,
                    "path": path,
                    "data": data
                })

            except Exception as e:
                print(f"Error loading {filename}: {e}")

    return documents


def get_document(document_name):
    """
    Returns a single knowledge document.

    Args:
        document_name (str): JSON filename

    Returns:
        dict | None
    """

    path = os.path.join(KNOWLEDGE_FOLDER, document_name)

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def count_entities(document):
    """
    Counts the total number of extracted entities.

    Args:
        document (dict)

    Returns:
        int
    """

    total = 0

    for entities in document.values():
        if isinstance(entities, list):
            total += len(entities)

    return total


def count_categories(document):
    """
    Counts how many categories contain at least one entity.

    Args:
        document (dict)

    Returns:
        int
    """

    count = 0

    for entities in document.values():
        if isinstance(entities, list) and len(entities) > 0:
            count += 1

    return count


def get_category_summary(document):
    """
    Returns the number of entities in each category.

    Args:
        document (dict)

    Returns:
        dict
    """

    summary = {}

    for category, entities in document.items():

        if isinstance(entities, list):
            summary[category] = len(entities)

    return summary