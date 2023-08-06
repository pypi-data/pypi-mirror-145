import asyncio
import dataclasses
import enum
import pathlib
import typing

import aioitertools.itertools
import clone_repo.clone
import clone_repo.parse_repo_url
import gidgethub.abc
import gidgethub.httpx
import httpx
import pydantic
import structlog


class GithubRepo(pydantic.BaseModel):
    name: str
    full_name: str
    git_url: str
    ssh_url: str
    clone_url: str


class GroupType(enum.Enum):
    user = "user"
    organization = "org"
    me = "me"


@dataclasses.dataclass
class Group:
    """Represents a user, organization or group within a repo hosting service

    Primarily used to determine which API to call.
    """

    type: GroupType
    name: str

    def __init__(self, name: str):
        if name == "me":
            self.type = GroupType.me
            self.name = "self"
        else:
            type, self.name = name.split(":", 1)
            self.type = GroupType(type)

    @property
    def github_api_repos_path(self) -> str:
        """Returns the appropriate API path to call in GitHub to list repos"""
        if self.type == GroupType.user:
            return f"users/{self.name}/repos"
        if self.type == GroupType.organization:
            return f"orgs/{self.name}/repos"
        if self.type == GroupType.me:
            return f"user/repos"
        raise ValueError(f"Can't handle {self.type}:{self.name}")


async def list_repos_for_group(
    group: Group, github: gidgethub.abc.GitHubAPI
) -> typing.AsyncIterable[GithubRepo]:
    """Iterate over all repos for a given user/org"""
    async for repo_json in github.getiter(group.github_api_repos_path):
        yield GithubRepo.parse_obj(repo_json)


async def list_repos(
    groups: list[Group], github: gidgethub.abc.GitHubAPI
) -> typing.AsyncIterable[GithubRepo]:
    """Iterate over all repos for given groups, removing duplicates"""
    log = structlog.get_logger()
    seen_repos: set[str] = set()
    repo_generators = [list_repos_for_group(group, github) for group in groups]
    async for repo in aioitertools.itertools.chain(*repo_generators):
        if repo.full_name not in seen_repos:
            yield repo
            seen_repos.add(repo.full_name)
        else:
            log.debug("Duplicate", repo=repo, key=repo.full_name)


async def clone_all_from_groups(
    groups: list[Group],
    requestor: str,
    oauth_token: str,
    prefix: pathlib.Path,
    no_act: bool,
    base_url: str,
) -> None:
    log = structlog.get_logger(requestor=requestor)

    async with httpx.AsyncClient() as client:
        gh = gidgethub.httpx.GitHubAPI(
            client, requestor, oauth_token=oauth_token, base_url=base_url
        )
        async for repo in list_repos(groups, gh):
            log.debug("Found repo", repo=repo)

            repo_url = clone_repo.parse_repo_url.parse_url(repo.ssh_url)
            assert repo_url is not None
            clone_path = clone_repo.clone.get_destination_path_for_repo(
                repo_url=repo_url, prefix_path=prefix
            )
            log.debug(
                "Path to clone to", repo=repo, clone_path=clone_path, repo_url=repo_url
            )
            if clone_path.exists():
                log.debug(
                    "Skipping", repo=repo, clone_path=clone_path, repo_url=repo_url
                )
                continue

            log.info("Will clone", repo=repo, clone_path=clone_path, repo_url=repo_url)

            await asyncio.to_thread(
                clone_repo.clone.clone,
                repo_url=repo_url,
                no_act=no_act,
                fetch=False,
                prefix_path=prefix,
            )
