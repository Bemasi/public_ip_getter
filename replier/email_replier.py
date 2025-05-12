import imaplib
import smtplib
import email
from email.message import EmailMessage
import time
import requests
import os

EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_USERNAME = os.environ['EMAIL_USERNAME']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
IMAP_SERVER = os.environ['IMAP_SERVER']
IMAP_PORT = int(os.environ.get('IMAP_PORT', 993))
SMTP_SERVER = os.environ['SMTP_SERVER']
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
CHECK_INTERVAL = int(os.environ.get('CHECK_INTERVAL', 60))

def get_public_ip():
    return requests.get("https://api.ipify.org").text

def send_response(to_address, public_ip):
    msg = EmailMessage()
    msg["Subject"] = "IP Pública de la Raspberry Pi"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address
    msg.set_content(f"La IP pública actual es: {public_ip}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Enviada IP a {to_address}")

def check_email():
    with imaplib.IMAP4(IMAP_SERVER, IMAP_PORT) as imap:
        imap.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        imap.select("INBOX")
        status, messages = imap.search(None, '(UNSEEN)')
        if status != "OK":
            print("Error al buscar correos")
            return

        for num in messages[0].split():
            _, msg_data = imap.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            from_addr = email.utils.parseaddr(msg["From"])[1]
            print(f"Nuevo correo de: {from_addr}")

            public_ip = get_public_ip()
            send_response(from_addr, public_ip)

            imap.store(num, '+FLAGS', '\\Seen')

if __name__ == "__main__":
    while True:
        try:
            check_email()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)
