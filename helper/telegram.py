import os
import requests

TELEGRAM_BOT_API_KEY = os.getenv('TELEGRAM_BOT')

def sendMessage(sender_id: int, message: str) -> None:
  
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API_KEY}/sendMessage"

    payload = {
        "chat_id": sender_id,
        "text": message
    }
    headers = {"Content-Type": "application/json"}

    requests.request("POST", url, json=payload, headers=headers)
