from urllib.parse import urljoin
from requests import Session
from comgate.http.Response import Response


class HttpClient:
    def __init__(self, session: Session, base_data: dict, base_url: str):
        self.session = session
        self.base_data = base_data
        self.base_url = base_url

    def get(self, relative_uri: str, data: dict) -> Response:
        data.update(self.base_data)
        response = self.session.get(urljoin(self.base_url, relative_uri), params=data)
        return Response(response)

    def post(self, relative_uri: str, data: dict) -> Response:
        data.update(self.base_data)
        response = self.session.post(urljoin(self.base_url, relative_uri), data=data)
        return Response(response)
