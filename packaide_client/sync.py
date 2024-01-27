import requests
from typing import Union
from urllib.parse import urlparse

from pydantic import BaseModel

ENDPOINT = "/pack"


DEFAULT_TOLERANCE = 0.1
DEFAULT_OFFSET = 5
DEFAULT_ROTATIONS = 4


class NestingRequest(BaseModel):
    """ A request to the Packaide server.

    This reflects the `NestingRequest` class in the `packaideServer`.
    """
    height: float
    width: float
    shapes: list[str]
    tolerance: float
    offset: float
    rotations: int


class PackaideClient(object):
    """ A synchronous client for accessing a Packaide server. """
    _api_url: str

    def __init__(self, url: str):
        self._api_url = (urlparse(url)
                         ._replace(path=ENDPOINT)
                         .geturl())

    def pack(self, shapes: Union[str, list[str]], width: int, height: int,
             tolerance: float = DEFAULT_TOLERANCE,
             offset: float = DEFAULT_OFFSET,
             rotations: int = DEFAULT_ROTATIONS
             ) -> list[str]:
        """ Perform an API to the Packaide Server

        Parameters:
            shapes (list[str]): A list of SVG strings (or an SVG string) to pack onto the sheet.
            width (int): The width of the sheet in inches.
            height (int): The height of the sheet in inches.
            tolerance (float): The tolerance of the packing algorithm. Defaults to 0.1.
            offset (float): The offset of the packing algorithm. Defaults to 5.
            rotations (int): The number of rotations to use. Defaults to 4.

        Raises:
            `ValueError` when:
                - Sheet size is too small to fit any shape
                - One shape is too large to fit onto sheet
        """
        if isinstance(shapes, str):
            shapes = [shapes]

        # create the request
        request = NestingRequest(
            height=height,
            width=width,
            shapes=shapes,
            tolerance=tolerance,
            offset=offset,
            rotations=rotations
        ).model_dump()

        with requests.post(self._api_url, json=request) as response:
            if response.status_code == 200:
                sheets = response.json()
                return sheets
            if response.status_code == 400:
                parsed = response.json()
                details = parsed['detail']
                raise ValueError(details)
