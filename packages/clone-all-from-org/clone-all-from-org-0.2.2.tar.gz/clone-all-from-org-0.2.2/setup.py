# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clone_all_from_org']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aioitertools>=0.10.0,<0.11.0',
 'click>=8.1,<9.0',
 'clone-repo>=0.2.0,<1.0.0',
 'gidgethub>=5.1,<6.0',
 'httpx>=0.22,<0.23',
 'pydantic>=1.9,<2.0',
 'rich>=12.0,<13.0',
 'structlog>=21.5,<22.0',
 'typer>=0.4,<0.5',
 'types-PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['clone-all-from-org = clone_all_from_org.main:app']}

setup_kwargs = {
    'name': 'clone-all-from-org',
    'version': '0.2.2',
    'description': 'CLI tool to clone all repos from a given organization or user',
    'long_description': "# clone-all-from-org\n\n- [Home](https://github.com/micktwomey/clone-all-from-org)\n- [PyPI](https://pypi.org/project/clone-all-from-org/)\n\nCLI tool to clone all repos from a given organization or user\n\nInstall into your Python project using `pip install clone-all-from-org`\n\nInstall as a CLI tool using [pipx](https://pypa.github.io/pipx/): `pipx install clone-all-from-org`.\n\n# What does this do?\n\nFor any given GitHub users or orgs (or yourself) this will enumerate all the repos you can see and clone them to a prefix. This allows you to keep up to date with any repos in the uses or orgs you follow.\n\nThis script requires a GitHub OAuth token, or Personal Access Token, to talk to the GitHub API. The easiest way to get one is to login with the [GitHub CLI tool](https://github.com/cli/cli). This script knows how to read the token from that tool's config.\n\nTo run give it a list of orgs to clone:\n\n```sh\nclone-all-from-org me org:codinggrace user:micktwomey\n# clones all the repos into ~/src/github.com/{organization or user}/{repo name}\n```\n\nThis tool recognizes:\n- `org:someorg` - a GitHub organization\n- `user:someuser` - GitHub user\n- `me` - yourself\n\nNote that the GitHub APIs will only show you publicly available repos for users and orgs by default. If you are a member of the organization you can see all repos (if you have access). `me` is a special case, this will show all repos you have access to (including your own private repos). If you used `user:your-username` it would only show your public repos.\n\n# Combining with gitup\n\nThis combines well with [gitup](https://github.com/earwig/git-repo-updater) to fetch all new repos and then update all your cloned repos:\n\n```sh\n# one off setup\npipx install gitup clone-all-from-org\ngitup -a ~/src/github.com\n\n# run periodically\nclone-all-from-org me org:my-org\ngitup --prune\n```\n\n# GitHub Enterprise\n\nYou can override the default base URl with `--base-url`. This is most useful for accessing GitHub Enterprise servers.\n\nTypically you'd need something like `https://git.example.com/api/v3/` as a base URl for enterprise:\n\n```sh\nclone-all-from-org --base-url https://git.example.com/api/v3/ me\n```\n",
    'author': 'Michael Twomey',
    'author_email': 'mick@twomeylee.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/micktwomey/clone-all-from-org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
