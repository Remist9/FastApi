import requests
import json

# Загружаем токен из сохранённого файла
try:
    with open("token.json", "r") as f:
        token_data = json.load(f)
except FileNotFoundError:
    print("[!] Файл token.json не найден. Сначала выполните login.py")
    exit(1)

token = token_data.get("access_token")

# Заголовки с токеном
headers = {
    "token": token
}

# Отправка запроса на logout
response = requests.post("http://127.0.0.1:8000/logout", headers=headers)

# Вывод результата
print("Status:", response.status_code)
print("Response:", response.json())
