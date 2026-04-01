import requests

# Recursive chat function definition
def chat(endpoint: str, model: str, system_prompt: str, previous_response_id: str | None = None):
    prompt = input("You: ")
    if prompt == "exit":
        return

    payload = {
        "model": model,
        "input": prompt,
        "temperature": 0.7,
        "system_prompt": system_prompt or "You are a helpful assistant.",
    }

    if previous_response_id:
        payload["previous_response_id"] = previous_response_id

    resp = requests.post(endpoint, json=payload, timeout=10)
    data = resp.json()

    msg = next((i for i in data.get("output", []) if i.get("type") == "message"), {})
    print("Assistant: " + msg.get("content", ""))

    chat(endpoint, model, system_prompt, data.get("response_id"))


# Define the endpoint, model, and system prompt
endpoint = "http://127.0.0.1:1234/api/v1/chat"
model = "mistral-small-3.2-24b-instruct-2506"
system_prompt = "You are a helpful assistant."

chat(endpoint, model, system_prompt)