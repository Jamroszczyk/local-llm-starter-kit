import dotenv
import os
from openai import AzureOpenAI

dotenv.load_dotenv()

endpoint = os.getenv("ENDPOINT")
deployment = "o4-mini"

subscription_key = os.getenv("KEY")
api_version = os.getenv("API_VERSION")

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def chat(messages: list[dict]):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": "I am going to Paris, what should I see?",
            }
        ],
        max_completion_tokens=40000,
        model=deployment
    )

    print(response.choices[0].message.content)

chat([
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    },
    {
        "role": "user",
        "content": "I am going to Paris, what should I see?",
    }
])