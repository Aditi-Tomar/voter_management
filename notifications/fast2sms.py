# notifications/fast2sms.py
import requests
import os

FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY')

def send_sms(phone_numbers, message):
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        'authorization': FAST2SMS_API_KEY,
        'Content-Type': "application/json"
    }
    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "flash": 0,
        "numbers": ",".join(phone_numbers)
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
