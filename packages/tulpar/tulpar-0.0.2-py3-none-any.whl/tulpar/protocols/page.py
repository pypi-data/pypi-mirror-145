"""
tulpar/protocols/page.py
Ian Kollipara
2022.04.04

Page Protocol
"""

# Imports
from typing import Protocol

from falcon import Request, Response

from .resource import HTML


class PageFunc(Protocol):

    """A Protocol to represent what a Page should look like.

    This class represents what a Page Function should look like. Since
    all pages are simply get requests, the function needs to have a
    set signature.
    """

    def __call__(self, req: Request, res: Response, *args) -> HTML:
        ...
