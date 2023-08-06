from .config import api_urls
import requests


def generate_token(username="", password="", api_url=api_urls["accounts"]) -> str:
    from getpass import getpass
    data = {
        "username": username or input("Username: "),
        "password": password or getpass("Password: "),
    }
    response = requests.post(f"{api_url}/login", json=data)
    if response and "access_token" in response.json():
        return response.json()["access_token"]
    raise Exception("[Error] Authentication failed.")
