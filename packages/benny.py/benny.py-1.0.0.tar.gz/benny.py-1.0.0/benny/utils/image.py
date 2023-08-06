from io import BytesIO
from typing import Union

class Image:
    def __init__(self, response) -> None:
        self.url = response.url
        self.resp = response

    def __str__(self) -> str:
        return self.url

    def read(self, bytesio = True) -> Union[bytes, BytesIO]:
        _bytes = self.resp.text
        if bytesio:
            return BytesIO(_bytes.encode("utf-8"))

        return _bytes