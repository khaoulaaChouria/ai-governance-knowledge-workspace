import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)


def ask_llm(system_prompt, user_prompt):

    response = client.responses.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        instructions=system_prompt,
        input=user_prompt,
    )

    return response.output_text