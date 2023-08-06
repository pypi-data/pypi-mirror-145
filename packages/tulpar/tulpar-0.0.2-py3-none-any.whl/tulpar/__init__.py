""" Tulpar

Tulpar is a Python SSR Framework built on top of Falcon and PonyORM.
It uses HATEOAS exclusively as its form of communication, with HTMX serving
to guide the frontend.

Tulpar Applications should be initialized with the Tulpar CLI.
"""

# Exports
from .config import TulparConfig
from .middleware import TulparMiddleware
from .page import Page
from .resource import Resource
from .tulpar import Tulpar, render
