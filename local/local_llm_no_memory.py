import requests

# Define the endpoint, model, and system prompt
endpoint = "http://127.0.0.1:1234/api/v1/chat"
model = "llama-3.2-3b-instruct"
system_prompt = "You are a helpful assistant."

def chat(endpoint: str, model: str, message: str, system_prompt: str):
    payload = {
        "model": model,
        "input": message,
        "temperature": 0.7,
        "system_prompt": system_prompt or "You extract city name from the text and return it in the given format.",
    }

    resp = requests.post(endpoint, json=payload, timeout=10)
    data = resp.json()

    msg = next((i for i in data.get("output", []) if i.get("type") == "message"), {})
    return msg.get("content", "")

# Chat with the model ONCE!

schema = """
Always return city name i mentioned in the following format, only provide the json, no text:
{
    "city": "name"
}

my text:

"""

prompt = input("You: ")

full_prompt = f"{schema}\n\n{prompt}"

response = chat(endpoint, model, full_prompt, system_prompt)
print("Assistant: " + response)
