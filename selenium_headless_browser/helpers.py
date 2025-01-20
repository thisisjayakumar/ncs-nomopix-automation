# myapp/helpers.py
import os
import requests
from dotenv import load_dotenv

def load_env():
    load_dotenv()

def get_auth_token():
    if os.path.exists('auth_token.txt'):
        with open('auth_token.txt', 'r') as f:
            return f.read().strip()
    return None

def save_auth_token(token):
    with open('auth_token.txt', 'w') as f:
        f.write(token)

def delete_test(test_id, auth_token):
    base_url = "https://api.allen-live.in/internal-bff/api/v1/tests/"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {auth_token}",
        # Add other headers as needed...
    }
    url = f"{base_url}{test_id}"
    
    response = requests.delete(url, headers=headers)
    return response
