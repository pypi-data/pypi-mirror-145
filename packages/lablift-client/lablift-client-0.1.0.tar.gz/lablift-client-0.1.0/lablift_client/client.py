import requests


class Client:
    def __init__(self, token) -> None:
        self.token = token

    def request(self, method: str, route: str, **kwargs) -> requests.Response:
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Bearer " + self.token
        response = getattr(requests, method)(route, **kwargs)
        if not response:
            raise Exception(
                f"[Error] Cannot query server for route {route}. {response.content}")
        if response.status_code == 401:
            raise Exception("Invalid token!")
        return response
