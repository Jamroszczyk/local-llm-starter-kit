import requests

# Define the endpoint, model, and system prompt
endpoint = "http://127.0.0.1:1234/api/v1/chat"
model = "llama-3.2-3b-instruct"
system_prompt = "You are a helpful assistant."

def chat(endpoint: str, model: str, message: str, system_prompt: str,full_data: bool = False):
    payload = {
        "model": model,
        "input": message,
        "temperature": 0.7,
        "system_prompt": system_prompt or "You extract city name from the text and return it in the given format.",
    }

    resp = requests.post(endpoint, json=payload, timeout=10)
    data = resp.json()

    msg = next((i for i in data.get("output", []) if i.get("type") == "message"), {})
    if full_data:
        return data
    else:
        return msg.get("content", "")


prompt = input("You: ")

response = chat(endpoint, model, prompt, system_prompt, full_data=False) # False for only the text response, True for the full data
print("Assistant: " + response)
