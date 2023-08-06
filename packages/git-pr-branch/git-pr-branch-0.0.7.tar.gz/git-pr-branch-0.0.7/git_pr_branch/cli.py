import os
import sys
from subprocess import CalledProcessError

import click

from .commands import prune as do_prune
from .commands import pull as do_pull
from .commands import show as do_show
from .commands import update as do_update
from .config import conf
from .repo import GitRepo
from .utils.cli import AliasedGroup
from .utils.setup import setup_config


@click.command(cls=AliasedGroup)
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True),
    help="Path to the configuration file",
)
@click.option(
    "-u",
    "--upstream-remote",
    help="Name of the remote for the upstream repo (default: origin)",
)
@click.option("-v", "--verbose/--no-verbose", help="Show more stuff")
@click.pass_context
def cli(ctx, config_path, upstream_remote, verbose):
    """Manage branches and pull-requests"""
    ctx.ensure_object(dict)

    if not os.path.exists(conf.path):
        setup_config()

    conf.load(config_path)

    if verbose:
        conf["verbose"] = verbose

    ctx.obj["repo"] = repo = GitRepo()

    if upstream_remote:
        repo.get_remote(upstream_remote).set_upstream()


def _wrap_command(command, ctx, *args, **kwargs):
    repo = ctx.obj["repo"]
    try:
        command(repo, *args, **kwargs)
    except CalledProcessError as e:
        click.secho(
            f'Command "{" ".join(e.cmd)}" failed! Aborting.', fg="bright_red", err=True
        )
        sys.exit(e.returncode)


@cli.command()
@click.pass_context
def show(ctx):
    """Show branches and pull requests"""
    _wrap_command(do_show, ctx)


@cli.command()
@click.option(
    "--remotes/--no-remotes",
    "prune_remotes",
    default=True,
    show_default=True,
    help="Also prune remote references",
)
@click.pass_context
def prune(ctx, prune_remotes):
    """Remove branches whose pull requests are closed"""
    _wrap_command(do_prune, ctx, prune_remotes)


@cli.command(alias="co")
@click.argument("pr-number", type=int)
@click.pass_context
def checkout(ctx, pr_number):
    """DEPRECATED: use the "pull" command now"""
    click.secho(
        'Deprecation warning: this command has been renamed to "pull"',
        err=True,
        fg="bright_red",
    )
    ctx.forward(pull)


@cli.command()
@click.argument("pr-number", type=int)
@click.pass_context
def pull(ctx, pr_number):
    """Downloads and checks out a pull request in a local branch"""
    _wrap_command(do_pull, ctx, pr_number)


@cli.command(alias="up")
@click.pass_context
def update(ctx):
    """Pull the current PR into a new sub-branch"""
    _wrap_command(do_update, ctx)
