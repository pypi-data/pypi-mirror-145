"""
blink/core/middleware.py
Ian Kollipara
2022.04.01

Middleware Class
"""

# Imports
from typing import Dict

from falcon import Request, Response


class TulparMiddleware:
    """TulparMiddleware is the base class that
    all middleware subclass. It contains all the needed
    methods for creating middleware, as well as links to more formal
    documentation found on the Falcon website.
    """

    def process_request(self, req: Request, res: Response):
        """
        Sourced from https://falcon.readthedocs.io/en/stable/api/middleware.html

        Process the request before routing it.

        Note:
            Because Falcon routes each request based on req.path, a
            request can be effectively re-routed by setting that
            attribute to a new value from within process_request().

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        raise NotImplementedError()

    def process_resource(
        self, req: Request, res: Response, resource: object, params: Dict
    ):
        """
        Sourced from https://falcon.readthedocs.io/en/stable/api/middleware.html

        Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """
        raise NotImplementedError()

    def process_response(
        self, req: Request, res: Response, resource: object, req_succeeded: bool
    ):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
            req_succeeded: True if no exceptions were raised while
                the framework processed and routed the request;
                otherwise False.
        """
        raise NotImplementedError()
