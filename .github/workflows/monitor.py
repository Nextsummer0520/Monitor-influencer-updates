import os
import requests
from bs4 import BeautifulSoup

URL = "https://kydschoice.com/"
SELECTOR = "h2.product-title"  # 需要修改的关键点！
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_current_product():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.select_one(SELECTOR).text.strip() if soup.select_one(SELECTOR) else None

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    )

if __name__ == "__main__":
    current = get_current_product()
    try:
        with open('last_product.txt', 'r') as f:
            last = f.read().strip()
    except FileNotFoundError:
        last = ""
    if current and current != last:
        print("New product:", current)
        send_telegram(f"🔥 新产品上架！\n{current}")
        with open('last_product.txt', 'w') as f:
            f.write(current)
