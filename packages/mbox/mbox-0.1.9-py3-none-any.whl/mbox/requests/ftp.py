import re
from urllib.request import urlopen

from requests import Response
from requests.adapters import BaseAdapter


def build_response(request, file):
    response = Response()
    response.request = request
    response.url = request.url
    response.raw = file
    response.status_code = 200
    return response


class FTPAdapter(BaseAdapter):
    def __init__(self):
        super().__init__()

    def send(self, request, **kwargs):
        file = urlopen(request.url, timeout=kwargs.get("timeout"))
        return build_response(request, file)
