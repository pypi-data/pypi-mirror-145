# clone-all-from-org

- [Home](https://github.com/micktwomey/clone-all-from-org)
- [PyPI](https://pypi.org/project/clone-all-from-org/)

CLI tool to clone all repos from a given organization or user

Install into your Python project using `pip install clone-all-from-org`

Install as a CLI tool using [pipx](https://pypa.github.io/pipx/): `pipx install clone-all-from-org`.

# What does this do?

For any given GitHub users or orgs (or yourself) this will enumerate all the repos you can see and clone them to a prefix. This allows you to keep up to date with any repos in the uses or orgs you follow.

This script requires a GitHub OAuth token, or Personal Access Token, to talk to the GitHub API. The easiest way to get one is to login with the [GitHub CLI tool](https://github.com/cli/cli). This script knows how to read the token from that tool's config.

To run give it a list of orgs to clone:

```sh
clone-all-from-org me org:codinggrace user:micktwomey
# clones all the repos into ~/src/github.com/{organization or user}/{repo name}
```

This tool recognizes:
- `org:someorg` - a GitHub organization
- `user:someuser` - GitHub user
- `me` - yourself

Note that the GitHub APIs will only show you publicly available repos for users and orgs by default. If you are a member of the organization you can see all repos (if you have access). `me` is a special case, this will show all repos you have access to (including your own private repos). If you used `user:your-username` it would only show your public repos.

# Combining with gitup

This combines well with [gitup](https://github.com/earwig/git-repo-updater) to fetch all new repos and then update all your cloned repos:

```sh
# one off setup
pipx install gitup clone-all-from-org
gitup -a ~/src/github.com

# run periodically
clone-all-from-org me org:my-org
gitup --prune
```

# GitHub Enterprise

You can override the default base URl with `--base-url`. This is most useful for accessing GitHub Enterprise servers.

Typically you'd need something like `https://git.example.com/api/v3/` as a base URl for enterprise:

```sh
clone-all-from-org --base-url https://git.example.com/api/v3/ me
```
