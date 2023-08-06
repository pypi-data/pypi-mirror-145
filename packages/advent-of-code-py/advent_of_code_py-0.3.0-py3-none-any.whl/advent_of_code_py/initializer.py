"""
initializer module which defines Initializer class for initializing advent of code
function runner
"""
from __future__ import annotations

import inspect
from typing import Callable, Dict, TypeVar

T = TypeVar("T")


class Initializer:
    """
    Initialize class which is used to initialize an advent of code function runner.
    Initialize create a basic class which is used for adding of different
    function of advent of code solution so all of functions can be easily run with
    one simple CLI tool.
    """

    function_list: Dict[str, Callable[[str], T]] = {}

    def add(self, **kwargs):
        """Add a function to a Initializer class"""
        self.function_list.update(kwargs)

    def extend(self, another_initializer: Initializer):
        """Extends initializer with addition of another initialier to it"""
        self.function_list.update(another_initializer.get_function_list())

    def run(self, function_alias: str):
        """Run a certain function by their name/alias"""
        self.function_list.get(function_alias)()

    def run_all(self):
        """Run all functions which are added to `Initializer`"""
        for function in self.function_list.values():
            function()

    def list_functions(self):
        """List all of the function and its alias"""
        for (keys, value) in self.function_list.items():
            print(
                "{:10} -> {}.{}".format(
                    keys, inspect.getmodule(value.getfunction()).__name__, value
                )
            )

    def get_function_list(self):
        """Return all function_list which contain function_alias and function"""
        return self.function_list
