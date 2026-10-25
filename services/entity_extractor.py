import json

from services.llm_service import ask_llm


def extract_entities(text):

    with open("prompts/entity_extractor.txt", "r") as file:
        system_prompt = file.read()

    response = ask_llm(
        system_prompt=system_prompt,
        user_prompt=text
    )
    

    entities = json.loads(response)

    return entities

