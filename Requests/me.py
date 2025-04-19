import requests
import json

try:
    with open("token.json", "r") as f:
        token_data = json.load(f)
except FileNotFoundError:
    print("[!] Token file not found. Run login_request.py first.")
    exit(1)

token = token_data.get("access_token")

headers = {
    "token": token  # или "Authorization": f"Bearer {token}" если ты используешь стандартный header
}

response = requests.get("http://127.0.0.1:8000/me", headers=headers)

if response.status_code == 200:
    print("[✓] Access granted:", response.json())
else:
    print("[!] Access denied:", response.status_code, response.text)
