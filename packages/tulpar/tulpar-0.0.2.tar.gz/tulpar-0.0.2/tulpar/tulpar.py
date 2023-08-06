"""
blink/blink.py
Ian Kollipara
2022.03.31

Tulpar Application Class Definition
"""

# Imports
from importlib import import_module
from os import listdir
from os.path import isdir
from typing import List, final

from falcon import App
from jinja2 import Environment, PackageLoader, select_autoescape
from pony.orm import Database

from .config import TulparConfig
from .protocols.resource import HTML
from .resource import ResourceType


@final
class Tulpar:
    """Tulpar

    Tulpar is the main application class of Tulpar Programs.
    It includes the registration of pages, the registration of api routes,
    the configuration of the database, the creation of the tempalate engine,
    among other things as well.

    It is not to be subclassed, but middleware may be given as a list of
    parameters.
    """

    def __new__(cls: type["Tulpar"]) -> "Tulpar":
        # This attempts to load the user config. If the file is not present, the
        # application crashes.
        try:
            cls.config: TulparConfig = import_module("config").config
        except ModuleNotFoundError as error:
            raise ModuleNotFoundError(
                "Config Module cannot be found, or does not exist"
            ) from error

        cls.db = Database()
        cls.template_env = Environment(
            loader=PackageLoader(cls.config.app_name), autoescape=select_autoescape()
        )
        cls.__app = App("text/html; charset=utf-8", middleware=cls.config.middleware)

        return cls()

    def __init__(self) -> None:
        Tulpar.db.bind(provider=self.config.db_params[0], **self.config.db_params[1])
        Tulpar.db.generate_mapping(create_tables=True)
        self.register_page_directory("pages", Tulpar.__app)
        self.register_api_directory("/api", Tulpar.__app)

    def register_page_directory(
        self, directory: str, app: App, route_prefix: str = ""
    ) -> None:
        """Register the directory contents as a page.

        Given a real directory, register the module classes as pages to the given
        application. Recurse down the directory tree, building a route prefix value
        with each recursive descent.

        This skips all files that begin with an underscore(_). This includes directories.
        """

        for module in filter(lambda module: module[0] != "_", listdir(directory)):
            if isdir(module):
                self.register_page_directory(module, app, f"{route_prefix}/{module}")

            else:

                module_path = route_prefix[1:].replace("/", ".")

                # This complex piece of code instantiates the
                # page class and assigns page to the new object.
                page = getattr(
                    import_module(f"{module_path}{module[:-3]}"),
                    module[:-3],
                )()

                # This handles the case of an index page
                # for a route. It assigns it to the route
                # prefix.
                if module[:-3] == "index":
                    app.add_route(route_prefix or "/", page)

                else:

                    route_uri = (
                        f"{route_prefix}/{module[:-3].replace('_', '-').lower()}"
                    )
                    app.add_route(route_uri, page)

    def register_api_directory(
        self, directory: str, app: App, route_prefix: str = "/api"
    ):
        """Register the directory as an api route.

        Given a valid directory, recursively add all the files as api routes. This
        is determined by classes denoted with @Resource Decorator. This also
        shows the path.

        In this case the route prefix adjusts for nested areas. Just like page
        variation, this skips all files that begin with an underscore(_), including
        directories.
        """

        for module in filter(lambda module: module[0] != "_", listdir(directory)):
            if isdir(module):
                self.register_api_directory(module, app, f"{route_prefix}/{module}")
            else:

                # This is the same as its page counterpart
                # It just gets the resource class name
                resource_cls = "".join(map(str.capitalize, module[:-3].split("_")))

                # In this case the resource is simply a list of
                # ResourceType, so there's no need to instantiate
                # an object.
                resources: List[ResourceType] = getattr(
                    import_module(f"api.{module[:-3]}"), resource_cls
                )

                for resource in resources:
                    app.add_route(f"/{directory}{resource.route}", resource.obj)


def render(template_name: str, **kwargs) -> HTML:
    """render the given template using the given args.

    Given a valid template address (which is assumed to be within "templates")
    render the given template with the extra args, passed as keyword args.
    """

    return HTML(Tulpar.template_env.get_template(template_name).render(kwargs))
