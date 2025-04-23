import requests

def send_sms(phone_number, message):
    url = "https://www.fast2sms.com/dev/bulk"

    api_key = "7hQvZk9fJTzBNDVGpbIiFneosd4lEg8tWCwmM0cyrPaYjS6HXxZGQ8eFKWm1TsvN0YX2poVJB4tlkhR9"  # Replace this with your actual API key

    headers = {
        'authorization': api_key,
        'Content-Type': 'application/json',
    }

    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'p',
        'numbers': phone_number,
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ SMS sent successfully.")
        try:
            print("📨 Response:", response.json())
        except ValueError:
            print("⚠️ Could not parse JSON. Raw response:")
            print(response.text)
    else:
        print("❌ Failed to send SMS.")
        print("🧾 Response:", response.text)

if __name__ == "__main__":
    number = input("Enter phone number: ")
    msg = input("Enter your message: ")
    send_sms(number, msg)

    if send_sms(number, msg):
        print("All good! ✅")
    else:
        print("Something went wrong. ❌")
