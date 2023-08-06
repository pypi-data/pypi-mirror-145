"""CLI commands."""

import click
from bancorml.utils.cli_utils import print_info


@click.group()
def cli():
    """CLI command with no arguments. Does nothing."""
    pass


@click.command()
def info():
    """CLI command with `info` argument. Prints info about the system, bancorml, and dependencies of bancorml."""
    print_info()


cli.add_command(info)
