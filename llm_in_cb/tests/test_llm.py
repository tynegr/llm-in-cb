# import requests
#
# url = "http://localhost:1349/completion"
#
# headers = {
#     "Content-Type": "application/json"
# }
#
# data = {
#     "prompt": "Hello, how are you?",
#     "max_tokens": 50
# }
#
# try:
#     response = requests.post(url, headers=headers, json=data)
#     response.raise_for_status()
#     result = response.json()
#     print("Response:", result)
# except requests.exceptions.RequestException as e:
#     print("Error:", e)


import requests

system_prompt = "You are an AI assistant"
prompt = "hi"

response = requests.post('http://localhost:11434/api/generate',
json={
"model": "llama3.2:1b",
"prompt": f"{system_prompt}\n\n{prompt}",
"stream": False
})

print(response.text)