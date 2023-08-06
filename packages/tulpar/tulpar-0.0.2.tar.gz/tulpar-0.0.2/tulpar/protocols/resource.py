"""
blink/core/protocols/resource.py
Ian Kollipara
2022.04.03

Resource Protocol Definition
"""

# Imports
from typing import NewType, Protocol, TypeVar

from falcon import Request, Response

HTML = NewType("HTML", str)

# Every class in this file is a protocol for forcing resource endpoints to
# implement a endpoint method. As such, it's quite repetitive.
# TODO Document the classes


class SupportsCheckin(Protocol):
    def on_checkin(self, req: Request, res: Response, *args) -> HTML:
        ...


CheckinsT = TypeVar("CheckinsT", bound=SupportsCheckin)


class SupportsCheckout(Protocol):
    def on_checkout(self, req: Request, res: Response, *args) -> HTML:
        ...


CheckoutsT = TypeVar("CheckoutsT", bound=SupportsCheckout)


class SupportsConnect(Protocol):
    def on_connect(self, req: Request, res: Response, *args) -> HTML:
        ...


ConnectsT = TypeVar("ConnectsT", bound=SupportsConnect)


class SupportsCopy(Protocol):
    def on_copy(self, req: Request, res: Response, *args) -> HTML:
        ...


CopiesT = TypeVar("CopiesT", bound=SupportsCopy)


class SupportsDelete(Protocol):
    def on_delete(self, req: Request, res: Response, *args) -> HTML:
        ...


DeletesT = TypeVar("DeletesT", bound=SupportsDelete)


class SupportsGet(Protocol):
    def on_get(self, req: Request, res: Response, *args) -> HTML:
        ...


GetsT = TypeVar("GetsT", bound=SupportsGet)


class SupportsHead(Protocol):
    def on_head(self, req: Request, res: Response, *args) -> HTML:
        ...


HeadsT = TypeVar("HeadsT", bound=SupportsHead)


class SupportsLock(Protocol):
    def on_lock(self, req: Request, res: Response, *args) -> HTML:
        ...


LocksT = TypeVar("LocksT", bound=SupportsLock)


class SupportsMkcol(Protocol):
    def on_mkcol(self, req: Request, res: Response, *args) -> HTML:
        ...


MkcolsT = TypeVar("MkcolsT", bound=SupportsMkcol)


class SupportsMove(Protocol):
    def on_move(self, req: Request, res: Response, *args) -> HTML:
        ...


MovesT = TypeVar("MovesT", bound=SupportsMove)


class SupportsOptions(Protocol):
    def on_options(self, req: Request, res: Response, *args) -> HTML:
        ...


OptionsT = TypeVar("OptionsT", bound=SupportsOptions)


class SupportsPatch(Protocol):
    def on_patch(self, req: Request, res: Response, *args) -> HTML:
        ...


PatchesT = TypeVar("PatchesT", bound=SupportsPatch)


class SupportsPost(Protocol):
    def __init__(self, *args, **kwargs) -> None:
        ...

    def on_post(self, req: Request, res: Response, *args) -> HTML:
        ...


PostsT = TypeVar("PostsT", bound=SupportsPost)


class SupportsPropfind(Protocol):
    def on_propfind(self, req: Request, res: Response, *args) -> HTML:
        ...


PropfindsT = TypeVar("PropfindsT", bound=SupportsPropfind)


class SupportsProppatch(Protocol):
    def on_proppatch(self, req: Request, res: Response, *args) -> HTML:
        ...


ProppatchesT = TypeVar("ProppatchesT", bound=SupportsProppatch)


class SupportsPut(Protocol):
    def on_put(self, req: Request, res: Response, *args) -> HTML:
        ...


PutsT = TypeVar("PutsT", bound=SupportsPut)


class SupportsReport(Protocol):
    def on_report(self, req: Request, res: Response, *args) -> HTML:
        ...


ReportsT = TypeVar("ReportsT", bound=SupportsReport)


class SupportsTrace(Protocol):
    def on_trace(self, req: Request, res: Response, *args) -> HTML:
        ...


TracesT = TypeVar("TracesT", bound=SupportsTrace)


class SupportsUncheckin(Protocol):
    def on_uncheckin(self, req: Request, res: Response, *args) -> HTML:
        ...


UncheckinsT = TypeVar("UncheckinsT", bound=SupportsUncheckin)


class SupportsUnlock(Protocol):
    def on_unlock(self, req: Request, res: Response, *args) -> HTML:
        ...


UnlocksT = TypeVar("UnlocksT", bound=SupportsUnlock)


class SupportsUpdate(Protocol):
    def on_update(self, req: Request, res: Response, *args) -> HTML:
        ...


UpdatesT = TypeVar("UpdatesT", bound=SupportsUpdate)


class SupportsVersionControl(Protocol):
    def on_version_control(self, req: Request, res: Response, *args) -> HTML:
        ...


VersionControlsT = TypeVar("VersionControlsT", bound=SupportsVersionControl)


class SupportsWebSocket(Protocol):
    def on_websocket(self, req: Request, res: Response, *args) -> HTML:
        ...


WebSocketsT = TypeVar("WebSocketsT", bound=SupportsWebSocket)

SupportsResources = (
    SupportsCheckin
    | SupportsCheckout
    | SupportsConnect
    | SupportsCopy
    | SupportsDelete
    | SupportsGet
    | SupportsHead
    | SupportsLock
    | SupportsMkcol
    | SupportsMove
    | SupportsOptions
    | SupportsPatch
    | SupportsPost
    | SupportsPropfind
    | SupportsProppatch
    | SupportsPut
    | SupportsReport
    | SupportsReport
    | SupportsTrace
    | SupportsUncheckin
    | SupportsUnlock
    | SupportsUpdate
    | SupportsVersionControl
    | SupportsWebSocket
)

ResourceT = TypeVar("ResourceT", bound=SupportsResources)
