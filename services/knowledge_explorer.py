from services.knowledge_repository import get_documents


def get_all_entities():

    documents = get_documents()

    knowledge = {}

    for document in documents:

        data = document["data"]

        for category, entities in data.items():

            if category not in knowledge:
                knowledge[category] = {}

            for entity in entities:

                entity_name = entity["name"].strip().lower()

                if entity_name not in knowledge[category]:

                    knowledge[category][entity_name] = {
                        "name": entity["name"],
                        "description": entity["description"],
                        "source_text": entity["source_text"],
                        "documents": [document["name"]]
                    }

                else:

                    if document["name"] not in knowledge[category][entity_name]["documents"]:
                        knowledge[category][entity_name]["documents"].append(document["name"])

    # Convert dictionaries to lists
    for category in knowledge:
        knowledge[category] = list(knowledge[category].values())

    return knowledge


def search_entities(query):

    knowledge = get_all_entities()

    results = {}

    query = query.lower().strip()

    for category, entities in knowledge.items():

        matches = []

        for entity in entities:

            name = entity["name"].lower()
            description = entity["description"].lower()

            if query in name or query in description:
                matches.append(entity)

        if matches:
            results[category] = matches

    return results