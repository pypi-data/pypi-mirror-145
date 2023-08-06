import click

from .main import (
    add_common_options,
    common_options,
    main,
)
from ..commands import TeamsCommand


@main.group(invoke_without_command=True)
def teams(*args, **kwargs):
    """Team related commands"""
    pass


@teams.command(name="list")
@add_common_options(common_options)
def list_command(**kwargs):
    """List all the teams

    List the team's slug by default. Use the --attrs option to change what
    attributes to show.
    """
    attrs = kwargs["attrs"] if kwargs["attrs"] else ["slug"]
    TeamsCommand(**kwargs).list_command(attrs)


@teams.command()
@add_common_options(common_options)
@click.option(
    "--team",
    required=True,
    help="""Show the members of a given team. Should be used with --role option
            to filter by roles.""",
)
def list_projects(**kwargs):
    """List all projects of a given team

    List a project's slug by default. Use the --attrs option to change what
    attributes to show.
    """
    attrs = kwargs["attrs"] if kwargs["attrs"] else ["slug"]
    TeamsCommand(**kwargs).list_projects(kwargs["team"], attrs)
