from .client import Client
from .config import api_urls
from typing import Union


class Biofeature:
    def __init__(self, client: Client) -> None:
        self.client = client

    def call(self, img: str, cpf: Union[None, str] = None) -> dict:
        response = self.client.request(
            "post", f"{api_urls['biofeatureai']}/predict", files={"file": open(img, 'rb')}, json={"cpf": cpf})
        if not response.status_code == 201:
            raise Exception(f"[Error] Prediction failed. {response.content}")
        return response.json()
