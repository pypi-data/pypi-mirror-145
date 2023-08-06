"""
tulpar/page.py
Ian Kollipara
2022.04.04

Page Decorator Definition
"""

# Imports
from functools import partial
from typing import Type

from .base_decorator import BaseDecorator
from .protocols.page import PageFunc


class Page(BaseDecorator):
    """Tulpar Page Decorator.

    This denotes what is a normal page in a Tulpar application.
    It allows for dependency injection just like a resource, but
    is handled differently behind the scenes. A page should be
    a function that has at least two parameters: req and res.

    Example:
    ```python
    @Page()
    def index(req, res):
        return HTML("<p>Hello World</p>")
    ```
    """

    def __call__(self, page_func: PageFunc) -> Type:
        cls_name = "".join(map(str.capitalize, page_func.__name__.split("_")))  # type: ignore
        page_with_deps = partial(page_func, **self.initialize_dependencies())
        cls = type(cls_name, (), {"on_get": page_with_deps})
        return cls
