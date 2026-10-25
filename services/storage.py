print("knowledge_storage.py is being imported")

import json
import os

def save_entities(document_name, entities):
    print("save_entities called")

    os.makedirs("knowledge", exist_ok=True)

    filename = os.path.splitext(document_name)[0] + ".json"
    path = os.path.join("knowledge", filename)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            entities,
            file,
            indent=4,
            ensure_ascii=False
        )

    return path