import re

import click
from tabulate import tabulate

from .config import conf
from .utils import get_ellipsised
from .utils.relationship import create_pr_branch, get_remote_for_pr


def pull(repo, pr_number):
    pr_branches = [
        b for b in repo.get_branches() if b.name.startswith(f"PR/{pr_number}/")
    ]
    origin_remote = repo.get_upstream_remote()
    origin_repo = origin_remote.get_server_repo()
    default_branch = origin_remote.get_default_branch()
    pr = origin_repo.get_pull(pr_number)

    if pr.state == "closed":
        answer = click.confirm("This PR is closed, are you sure you want to pull it?")
        if not answer:
            click.echo("Aborting.")
            return

    # Move to the default branch
    default_branch.checkout(quiet=True)
    # Get or create the remote for this PR
    remote = get_remote_for_pr(repo, pr)
    remote.fetch(quiet=True)
    branch_id = len(pr_branches) + 1
    if branch_id == 1:
        # Initial checkout: also check out previous reviews
        for review in pr.get_reviews():
            if review.username == pr.username:
                # Review requests show up as review comments in the API
                continue
            if review.state == "PENDING":
                continue
            timestamp = review.datetime.strftime("%x %X")
            click.secho(
                f"Checking out review by {review.username} on {timestamp} with state "
                f"{review.state} to sub-branch {branch_id}",
                fg="bright_cyan",
            )
            create_pr_branch(pr, branch_id, remote, review.commit_id)
            branch_id += 1

    click.secho(
        f"Checking out PR #{pr.number} to sub-branch {branch_id}", fg="bright_cyan"
    )
    branch = create_pr_branch(pr, branch_id, remote, pr.head_commit)
    branch.checkout()


def prune(repo, prune_remotes):
    to_prune = []
    origin_remote = repo.get_upstream_remote()
    origin_repo = origin_remote.get_server_repo()
    click.echo("Branches to prune:")
    for branch in repo.get_branches():
        pulls = origin_repo.get_pulls(branch)
        if not pulls:
            continue
        if all([pr.state == "closed" for pr in pulls]):
            click.echo(branch.name)
            to_prune.append(branch)
    if to_prune:
        answer = click.confirm("Should they be deleted locally?")
        if answer:
            current_branch = repo.get_current_branch()
            default_branch = origin_remote.get_default_branch()
            if current_branch in to_prune:
                default_branch.checkout()
            for branch in to_prune:
                branch.delete(force=True)
        else:
            click.echo("OK, aborting here.")
    else:
        click.echo("No branch to prune.")
    if prune_remotes:
        click.secho("Cleaning up remote references", fg="bright_cyan")
        for remote in repo.get_remotes():
            remote.prune()


def show(repo):
    branches = repo.get_branches()
    origin_repo = repo.get_upstream_remote().get_server_repo()
    if not conf["quiet"]:
        click.secho("Gathering data...", fg="bright_cyan")
    data = []
    for branch in branches:
        branch_data = [branch.name]
        pulls = origin_repo.get_pulls(branch)
        if not pulls:
            data.append(branch_data)
            continue
        branch_data.append("\n".join(f"#{pr.number}" for pr in pulls))
        branch_data.append("\n".join(f"[{pr.state}]" for pr in pulls))
        branch_data.append("\n".join(get_ellipsised(pr.title, 80) for pr in pulls))
        branch_data.append("\n".join(pr.html_url for pr in pulls))
        data.append(branch_data)
    click.echo(tabulate(data, headers=["Branch", "PR", "State", "Title", "URL"]))


def update(repo):
    branch = repo.get_current_branch()
    match = re.match(r"PR/([0-9]+)/[0-9]+", branch.name)
    if not match:
        raise click.ClickException(
            "Could not extract the PR number from the branch name, you'll have to use "
            "the pull command."
        )
    branch.copy("PR/prev")
    pr_branch = int(match.group(1))
    pull(repo, pr_branch)
    click.echo("The PR's previous version is in PR/prev")
