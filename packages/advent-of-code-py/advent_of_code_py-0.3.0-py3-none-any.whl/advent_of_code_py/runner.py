"""advent of code runner for creating CLI for solution for easy execution"""
import click


def advent_runner(func):
    """
    Advent of code runner decorator which decorates a function for a simple CLI
    tool creation. Function which is decorated using a advent of code runner should
    return a Initializer class so it can create a CLI from Initializer class object
    """

    def create_command():
        initializer_defined = func()

        @click.group(help="CLI tool created from a provided Initializer Object")
        def main():
            pass

        @main.command(
            "run", help="run a certain function by name present in Initializer"
        )
        @click.argument("name")
        def run_function(name):
            initializer_defined.run(name)

        @main.command("all", help="run all function defined in a Initializer class")
        def run_all_function():
            initializer_defined.run_all()

        @main.command("list", help="list all of the available function")
        def list_functions():
            initializer_defined.list_functions()

        return main()

    return create_command
