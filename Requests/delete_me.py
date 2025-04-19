import requests
import json

# Загружаем токен из файла
try:
    with open("token.json", "r") as f:
        token_data = json.load(f)
except FileNotFoundError:
    print("[!] token.json не найден. Сначала выполните login.py")
    exit(1)

token = token_data.get("access_token")

# Заголовки
headers = {
    "token": token
}

# Отправка запроса на удаление
response = requests.delete("http://127.0.0.1:8000/delete_me", headers=headers)

# Вывод результата
print("Status:", response.status_code)
print("Response:", response.json())
