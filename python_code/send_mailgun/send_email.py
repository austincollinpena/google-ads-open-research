import requests
import os


def send_email(to: str, subject: str, body: str):
    resp = requests.post(
        'https://api.mailgun.net/v3/mail.googleadsopenresearch.com/messages',
        auth=("api", os.getenv('mailgun_key')),
        data={
            "from": "auto@mail.googleadsopenresearch.com",
            "to": to,
            "subject": subject,
            "text": body,
            "h:Reply-To": "Austin Pena <austin@googleadsopenresearch.com>"
        }
    )
    if resp.status_code != 200:
        print(resp.text)


if __name__ == '__main__':
    send_email('me@austinpena.com', 'test email', 'test body')
