import os

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_EMBEDDING_API_KEY"),
    api_version="2025-03-01-preview",
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT")
)
def generate_embedding(text: str):

    response = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        input=text
    )

    return response.data[0].embedding
if __name__ == "__main__":

    embedding = generate_embedding(
        "Top Management is responsible for AI governance."
    )

    print(len(embedding))