import os
import requests

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BOT_ADMIN = os.getenv("TELEGRAM_BOT_ADMIN")
TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(data):
        if not (TELEGRAM_BOT_ADMIN and TELEGRAM_BOT_TOKEN):
            raise ValueError('TELEGRAM_BOT_ADMIN or TELEGRAM_BOT_TOKEN variables are not set up.')
        chat_data = {}
        chat_data['chat_id'] = TELEGRAM_BOT_ADMIN
        chat_data['text'] = str(data)
        reply = requests.post(TELEGRAM_BASE_URL, json=chat_data)
        if reply.status_code > 299:
            raise ValueError('Bad reply from telegram.')

