import asyncio
import logging
import pathlib
import typing
import urllib.parse

import structlog
import structlog.contextvars
import structlog.processors
import typer
import yaml

from .clone_all_from_org import Group, clone_all_from_groups

app = typer.Typer()


async def mainloop(
    prefix: pathlib.Path,
    groups: list[Group],
    oauth_token: str,
    no_act: bool,
    base_url: str,
) -> None:
    await clone_all_from_groups(
        groups,
        "https://github.com/micktwomey/clone-all-from-org",
        oauth_token,
        prefix,
        no_act,
        base_url,
    )


@app.command()
def main(
    groups: list[str] = typer.Argument(
        ...,
        metavar="group",
        help="Users or organizations to clone from. Use user:name, me or org:name.",
    ),
    prefix: str = typer.Option(
        "~/src", help="Prefix to clone to. Will clone to `{prefix}/{host}/{org}/{repo}`"
    ),
    base_url: str = typer.Option(
        "https://api.github.com",
        help="GitHub base API URL to talk to. Change to use GitHub enterprise servers.",
    ),
    verbose: bool = typer.Option(
        False, "--verbose/--no-verbose", "-v", help="Enable more verbose log output"
    ),
    debug: bool = typer.Option(
        False, "--debug/--no-debug", "-d", help="Enable more debug log output"
    ),
    json: bool = typer.Option(
        False,
        "--json/--no-json",
        "-j",
        envvar="CLONE_REPO_JSON_LOGS",
        help="Use JSON for log output",
    ),
    no_act: bool = typer.Option(
        False, "--no-act/--act", "-n", help="Simulate the clone"
    ),
    oauth_token: typing.Optional[str] = typer.Option(
        None, envvar="CLONE_ALL_FROM_ORG_OAUTH_TOKEN", help="GitHub API token"
    ),
) -> None:
    """Clone all repos from a given org.

    If the repo exists then skip.
    """
    clone_prefix = pathlib.Path(prefix).expanduser().resolve()

    processors: list[structlog.types.Processor] = (
        [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
        if json
        else [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ]
    )

    structlog.configure(
        cache_logger_on_first_use=True,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if verbose else (logging.DEBUG if debug else logging.WARNING)
        ),
        processors=processors,
    )

    log = structlog.get_logger()

    try:
        if oauth_token is None:
            # Fish for the token from the gh client config
            gh_config_path = (
                pathlib.Path("~/.config/gh/hosts.yml").expanduser().resolve()
            )
            if not gh_config_path.is_file():
                raise ValueError(
                    f"Neither CLONE_ALL_FROM_ORG_OAUTH_TOKEN is present in env nor {gh_config_path} readable from gh client."
                )
            host = urllib.parse.urlparse(base_url).hostname
            if host is None:
                raise ValueError(f"Can't figure out hostname from {base_url}")
            with gh_config_path.open("rb") as fp:
                gh_config = yaml.safe_load(fp)
                if host not in gh_config and host.startswith("api."):
                    # try dropping the api.
                    host = host[len("api.") :]
                try:
                    oauth_token = gh_config[host]["oauth_token"]
                except KeyError:
                    raise ValueError(
                        f"Can't find a valid oauth_token for {base_url} in {gh_config_path}, try a 'gh auth login' to authenticate or check your base url."
                    )
        structlog.contextvars.reset_contextvars()
        structlog.contextvars.bind_contextvars(
            prefix=clone_prefix,
            verbose=verbose,
            debug=debug,
            json=json,
            no_act=no_act,
            groups=len(groups),
            oauth_token="*" * len(oauth_token),
            base_url=base_url,
        )
        log.debug("main")
        asyncio.run(
            mainloop(
                clone_prefix,
                [Group(g) for g in groups],
                oauth_token,
                no_act,
                base_url,
            )
        )
    except Exception as e:
        log.exception(f"Failed to clone repos: {e}", exc_info=debug or json, error=True)
        raise typer.Exit(code=1)
    log.info("Finished cloning repos", error=False)


if __name__ == "__main__":
    app()
