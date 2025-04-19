import requests
import json

login_data = {
    "login": "Login",
    "password": "Password"
}

response = requests.post("http://127.0.0.1:8000/login", json=login_data)

if response.status_code == 200:
    token_data = response.json()
    with open("token.json", "w") as f:
        json.dump(token_data, f)
    print("[✓] Token saved to token.json")
else:
    print("[!] Login failed:", response.status_code, response.text)
