import requests

# Credentials
EMAIL = "ginmail9878@punkproof.com"
PASSWORD = "VhZ7qx6GHcs9"
BASE_URL = "https://api.mail.tm"

# 1. Get token
def get_token(email, password):
    response = requests.post(f"{BASE_URL}/token", json={
        "address": email,
        "password": password
    })
    response.raise_for_status()
    return response.json()["token"]

# 2. Get messages
def get_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/messages", headers=headers)
    response.raise_for_status()
    return response.json()["hydra:member"]

# 3. Fetch and print message dates
def print_message_dates(email, password):
    token = get_token(email, password)
    messages = get_messages(token)
    if not messages:
        print("No messages found.")
        return
    for msg in messages:
        print(f"Subject: {msg['subject']}")
        print(f"From: {msg['from']['address']}")
        print(f"Date: {msg['createdAt']}")
        print("-" * 40)

print_message_dates(EMAIL, PASSWORD)
