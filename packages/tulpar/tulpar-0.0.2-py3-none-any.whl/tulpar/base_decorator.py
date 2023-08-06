"""
tulpar/base_decorator.py
Ian Kollipara
2022.04.04

Base Class for all decorator classes
"""
# Imports
from re import compile as re_compile
from typing import Any, Callable, Dict, List, Optional, TypedDict


class Dependency(TypedDict):
    """Dependency Type for use in Dependency Injection

    This dictionary type represents what a dependency could look like
    for Blink.
    """

    dependency: Callable
    dependency_params: Optional[Dict[str, Any] | List[Any]]


class BaseDecorator:
    """This is the base class from which all Tulpar decorators inherit from.

    Tulpar decorators usually need a set of methods, as well as a way to
    deal with dependencies. This allows for that.
    """

    def __init__(self, dependencies: Optional[List[Dependency]] = None) -> None:
        self.dependencies = dependencies
        self.camel_to_snake_pattern = re_compile(r"(?<!^)(?=[A-Z])")

    def camel_case_to_snake(self, camel_case: str) -> str:
        """Transform a CamelCase string to snake_case.

        Given a valid string, return the lowered, snake_case
        version of that string.
        """

        return self.camel_to_snake_pattern.sub("_", camel_case).lower()

    def initialize_dependencies(self) -> Dict[str, object]:
        """Initialize the decoratorated class' dependencies.

        Given that the dependencies are not None, initialize each
        with the given parameters and return the collection of initialized
        dependencies.
        """

        initialized_deps: Dict[str, object] = {}
        for dep in self.dependencies or []:

            if isinstance(dep["dependency_params"], list):
                initialized_deps |= {
                    self.camel_case_to_snake(dep["dependency"].__name__): dep[
                        "dependency"
                    ](*dep["dependency_params"])
                }

            elif isinstance(dep["dependency_params"], dict):
                initialized_deps |= {
                    self.camel_case_to_snake(dep["dependency"].__name__): dep[
                        "dependency"
                    ](**dep["dependency_params"])
                }

            else:
                initialized_deps |= {
                    self.camel_case_to_snake(dep["dependency"].__name__): dep[
                        "dependency"
                    ]()
                }

        return initialized_deps
