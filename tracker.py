import requests
import re
import smtplib
import os
from email.message import EmailMessage
from bs4 import BeautifulSoup

URL = "https://www.zapateriafebo.com/products/zapato-feliz-1?variant=47301152866535"
HEADERS = {"User-Agent": "Mozilla/5.0"}

PRICE_LIMIT = 150000  # Precio objetivo

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

def get_price():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()

    match = re.search(r"\$\s?\d{1,3}(\.\d{3})+", text)
    if not match:
        return None

    price = int(match.group().replace("$", "").replace(".", "").strip())
    return price

def send_email(price):
    msg = EmailMessage()
    msg["Subject"] = "🔻 Bajó el precio del Zapato Feliz"
    msg["From"] = EMAIL
    msg["To"] = TO_EMAIL
    msg.set_content(f"El precio bajó a ${price}\n\n{URL}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

def main():
    price = get_price()
    print("Precio actual:", price)

    if price and price < PRICE_LIMIT:
        send_email(price)
        print("Email enviado")
    else:
        print("Sin cambios")

if __name__ == "__main__":
    main()
