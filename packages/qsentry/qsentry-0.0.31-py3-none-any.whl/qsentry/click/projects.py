import click

from .main import (
    add_common_options,
    common_options,
    main,
)
from ..commands import ProjectsCommand


common_projects_options = [
    click.option(
        "--project",
        required=True,
        help="""The project slug""",
    )
]


@main.group(invoke_without_command=True)
def projects(*args, **kwargs):
    """Project related commands"""
    pass


@projects.command()
@add_common_options(common_options)
@add_common_options(common_projects_options)
def list_keys(**kwargs):
    """List all client keys of the given project.

    List the key's id, dsn and rate limit by default. Use the --attrs option to
    change what attributes to show.
    """
    attrs = kwargs["attrs"] if kwargs["attrs"] else ["id", "dsn", "rateLimit"]
    ProjectsCommand(**kwargs).list_keys(kwargs["project"], attrs)


@projects.command()
@add_common_options(common_options)
@add_common_options(common_projects_options)
@click.option(
    "--id",
    "key_id",
    required=True,
    help="""The id of the client key to be updated""",
)
@click.option(
    "--data",
    required=True,
    help="""The JSON data used to update the key""",
)
def update_key(**kwargs):
    """Update a client key."""
    ProjectsCommand(**kwargs).update_key(
        kwargs["project"], kwargs["key_id"], kwargs["data"]
    )
