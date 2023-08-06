from requests import Response as RequestsResponse
from urllib.parse import parse_qsl


class Response:
    parsed_content = None

    def __init__(self, response: RequestsResponse):
        self.response = response

    def get_status_code(self) -> int:
        return self.response.status_code

    def is_ok(self) -> bool:
        return self.get_parsed_body().get('code') == '0'

    def get_data(self) -> dict:
        return self.get_parsed_body()

    def get_parsed_body(self) -> dict:
        if not self.parsed_content:
            if self.response.headers.get('Content-Type').startswith('application/json'):
                self.parsed_content = self.response.json()
            else:
                self.parsed_content = dict(parse_qsl(self.response.content.decode('UTF-8')))
        return self.parsed_content
