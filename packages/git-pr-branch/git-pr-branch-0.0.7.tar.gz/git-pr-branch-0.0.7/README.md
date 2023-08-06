# GIT PR branch

`git-pr-branch` is a command line tool designed to manage the relationship between branches and
pull-requests.

At the moment it only supports Github and Pagure, but other backends are possible.

You need to create a personal token in [your Github settings
page](https://github.com/settings/tokens) if you plan to use Github (Pagure can work without a
token). When you start the program for the first time, it will ask you for it and store it in a
configuration file.

## Downloading pull requests

`git pr-branch pull 42` will download pull request #42 in a local branch, creating a new branch each
time the command is run. Why, you ask? Because it is common for PR authors to amend their commits
after a review instead of adding more commits, and as a reviewer it's hard to see the differences
between the code you reviewed and the new code. By creating a new branch each time, you can just
diff with the previous branch.

If you have not checked out this PR before, it will create a branch for every existing review in the
PR's history. This way it'll be easy to see what's changed between earlier reviews even if you did
not run the command at that time (this behavior is not supported on Pagure).

When you're working on the PR branch, running `git pr-branch update` or `git pr-branch up` will
download the latest version of the PR in a new branch and switch to it. It is a shortcut to running
the same command, so you don't have to remember and type in the PR number again.

## Displaying branches and pull requests

`git pr-branch show` will list all your local branches and show you whether they are associated with
a pull request, whether that PR is still open or not, and the URL for that PR.

## Purging branches

`git pr-branch purge` will delete the branches that are linked to a closed pull request (or multiple
pull requests that are all closed). This will let you keep your local repo tidy.

## Options

If the remote name for the repository you're forking from (here called "upstream") is not named
"origin", you can set which remote is your upstream with the `-u` or `--upstream` option. Here is an
example: if Bob wants to fork Alice's repository he may clone his own fork first and then add
Alice's repository as a remote:

    $ git clone git@github.com:/bob/repo
    $ git remote add upstream git@github.com:/alice/repo

The original repository is therefore not in the default `origin` remote but in the `upstream` remote.
In this configuration, `git-pr-branch` must be used with the `-u` option as such:

    $ git pr-branch -u upstream show

The value will be set in the local repository's configuration and you won't need to use the option
in the future.

If most of your local repositories don't use the remote `origin` as upstream, you can configure a
different default value in the configuration file. The first-time setup "wizard" will ask you.
