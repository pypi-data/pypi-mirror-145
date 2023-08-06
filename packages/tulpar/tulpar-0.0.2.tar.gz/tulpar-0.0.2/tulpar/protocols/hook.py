"""
blink/core/hook.py
Ian Kollipara
2022.04.02

Hook Protocol Class Definition
"""

# Imports
from typing import Any, Dict, Protocol

from falcon import Request, Response


class Hook(Protocol):
    """Hook Protocol Definition

    Falcon provides a great interface for creating
    Hooks, but there's a lack of typing. As such, this
    exists to force a specific type for the hook.

    This only defines a call_method, so a function could
    potentially work as well.
    """

    def __call__(
        self, req: Request, res: Response, resource: object, param: Dict
    ) -> Any:
        ...
