import requests

response = requests.post("http://localhost:8000/register", json={
    "login": "Login",
    "password": "Password"
})

print("Status:", response.status_code)
print("Response:", response.json())
