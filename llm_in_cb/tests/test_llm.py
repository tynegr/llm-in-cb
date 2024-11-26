import requests

url = "http://localhost:1349/completion"

headers = {
    "Content-Type": "application/json"
}

data = {
    "prompt": "Hello, how are you?",
    "max_tokens": 50
}

try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    print("Response:", result)
except requests.exceptions.RequestException as e:
    print("Error:", e)
