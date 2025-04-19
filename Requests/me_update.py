import requests
import json

with open("token.json", "r") as f:
    token = json.load(f)["access_token"]

headers = {
    "token": token,
    "Content-Type": "application/json"
}

payload = {
    "firstname": "Oleg",
    "surname": "Иванов",
    "location": "Россия"
}

response = requests.put("http://127.0.0.1:8000/me/update", headers=headers, json=payload)

print("Status:", response.status_code)
print("Response:", response.json())
