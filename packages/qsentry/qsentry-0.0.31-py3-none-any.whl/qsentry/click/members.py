import click

from .main import (
    add_common_options,
    common_options,
    main,
)
from ..commands import MembersCommand


@main.group(invoke_without_command=True)
def members(*args, **kwargs):
    """Member related commands"""
    pass


@members.command(name="list")
@add_common_options(common_options)
@click.option(
    "--all",
    is_flag=True,
    help="""List all members of an organization. It shows the member's id and
            email by default. Use the --attrs option to change what attributes
            to show.""",
)
@click.option(
    "--team",
    help="""Show the members of a given team. Should be used with --role option
            to filter by roles.""",
)
@click.option(
    "--role", default="admin", show_default=True, help="The role of the member."
)
def list_command(**kwargs):
    """List members"""
    MembersCommand(**kwargs).list_command(**kwargs)


@members.command()
@add_common_options(common_options)
@click.argument("search_by_term")
def search_by(**kwargs):
    """Search a member by a term.

    The term should be in "<attribute>=<value>" form, for example "id=1234" or
    "email=foo@example.com", etc.
    """
    MembersCommand(**kwargs).search_by(kwargs["search_by_term"])
