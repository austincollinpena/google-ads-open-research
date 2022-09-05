import requests
import os


def send_email(to: str, subject: str, body: str):
    requests.post(
        'https://api.mailgun.net/v3/mail.googleadsopenresearch.com/messages',
        auth=("api", os.getenv('mailgun_key')),
        headers={
            'h:Reply-To': 'austin@googleadsopenresearch.com'
        },
        data={
            "from": "auto@mail.googleadsopenresearch.com",
            "to": to,
            "subject": subject,
            "text": body,
        }
    )
