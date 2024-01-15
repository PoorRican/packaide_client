import requests
from typing import Union
from urllib.parse import urlparse

ENDPOINT = "/pack"


class PackaideClient(object):
    """ A synchronous client for accessing a Packaide server. """
    _api_url: str

    def __init__(self, url: str):
        self._api_url = (urlparse(url)
                         ._replace(path=ENDPOINT)
                         .geturl())

    def pack(self, shapes: Union[str, list[str]], width: int, height: int) -> list[str]:
        """ Perform an API to the Packaide Server

        Parameters:
            shapes (list[str]): A list of SVG strings (or an SVG string) to pack onto the sheet.
            width (int): The width of the sheet in inches.
            height (int): The height of the sheet in inches.

        Raises:
            `ValueError` when:
                - Sheet size is too small to fit any shape
                - One shape is too large to fit onto sheet
        """
        if isinstance(shapes, str):
            shapes = [shapes]

        # create the request
        request = {
            "height": height,
            "width": width,
            "shapes": shapes,
        }

        with requests.post(self._api_url, json=request) as response:
            if response.status_code == 200:
                sheets = response.json()
                return sheets
            if response.status_code == 400:
                parsed = response.json()
                details = parsed['detail']
                raise ValueError(details)
