"""This module provides commands related to generating
documentation.

The `docs build` and `docs serve` commands invoke the respective
`mkdocs` command.

??? info "Adding new commands"

    Most commands in this file are wrappers around the `mkdocs` commandline. 
    The pattern described in [Click documentation for handling unknown options](https://click.palletsprojects.com/en/7.x/advanced/#forwarding-unknown-options)
    is useful for creating commands that invoke other commands.


"""
from subprocess import call
import os, shutil
import click
import flask
from pathlib import Path

INIT_SUCCESS_MESSAGE = 'Initialized documentation in "{}" folder'
INIT_ALREADY_MESSAGE = 'Cannot initialized documentation in "{}". File already exists'
BUILD_SUCCESS_MESSAGE = 'Succesfuly built documentation in {}.'
def project_path():
    path = '.'
    if flask.has_app_context() and flask.current_app:
        path = os.path.join(os.path.dirname(flask.current_app.root_path))
    return path


cli = click.Group("docs", help="Generate or serve documentation")


def run_mkdocs(mkdocs_yaml, command, verbose=False, args=None):
    """Invoke the `mkdocs` commandline."""

    args = args or []

    if verbose:
        args = ["--verbose"] + list(args)

    cmdline = ["mkdocs", command, "--config-file", str(mkdocs_yaml)] + list(args)

    if verbose:
        click.echo("Invoking: %s" % " ".join(cmdline))

    rv = call(cmdline)
    if rv != 0:
        exit(rv)


def interrogate_check(path="."):
    """Checks code base for missing docstrings."""

    rv = call("which interrogate".split())
    if rv != 0:
        print('Executable for "interrogate" not found. Try "pip install -e .[docs]"')
        exit(rv)

    rv = call(f"interrogate -vvv {path}".split())
    if rv != 0:
        exit(rv)


@cli.command("init")
@click.argument("path", required=False, default='.')
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def init_docs(verbose, path):
    """Initialize the documentation."""
    docs_dir = Path(path) / "docs"
    docs_template = Path(__file__).parent.parent / 'docs_template'

    shutil.copytree(docs_template, docs_dir)
    click.echo(INIT_SUCCESS_MESSAGE.format(docs_dir))

@cli.command("build", context_settings=dict(ignore_unknown_options=True))
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
@click.argument("path", required=False, default='.')
@click.argument("mkdocs_args", nargs=-1, type=click.UNPROCESSED)
def build_docs(verbose, path, mkdocs_args):
    """Build the documentation."""
    mkdocs_yaml = Path(path) / "docs" / "mkdocs.yml"
    run_mkdocs(
        mkdocs_yaml=mkdocs_yaml.absolute(), command="build", verbose=verbose, args=mkdocs_args
    )
    click.echo(BUILD_SUCCESS_MESSAGE.format(mkdocs_yaml))


@cli.command("serve", context_settings=dict(ignore_unknown_options=True))
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
@click.option("--no-dirtyreload", is_flag=True, help="Do cleanup on reload (slow)")
@click.argument("mkdocs_args", nargs=-1, type=click.UNPROCESSED)
def serve_docs(verbose, no_dirtyreload, mkdocs_args):
    """Start the documentation server with live reloading"""
    mkdocs_yaml = os.path.join(project_path(), "docs", "mkdocs.yml")
    if not no_dirtyreload:
        mkdocs_args = list(mkdocs_args)
        mkdocs_args.append("--dirtyreload")
    run_mkdocs(
        mkdocs_yaml=mkdocs_yaml, command="serve", verbose=verbose, args=mkdocs_args
    )


@cli.command("check")
@click.argument("path", required=False, default='.')
def check_docs(path):
    """
    Checks code base for missing docstrings.

    PATH is the file path of the code base to check.
    """

    interrogate_check(path=path)


try:
    from changelog import commands

    commands.cli.help = "Manage the project CHANGELOG.md files"
    cli.add_command(commands.cli, name="cl")
except ImportError as e:
    click.echo(
        err=True,
        message=f'Missing "changelog-cli" package. Try "pip install -e .[docs]"',
    )


def init_app(app: flask.Flask):
    """Initialize documentation commands"""
    app.cli.add_command(cli)
