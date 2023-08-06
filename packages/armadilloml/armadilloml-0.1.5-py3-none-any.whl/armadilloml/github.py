import os
import rich_click as click
from github import Github
from github.Repository import Repository
from rich.console import Console

console = Console()
github = Github(os.environ.get("GITHUB_TOKEN"))


def check_github_token():
    """
    Check if the github token is set.
    """
    if os.environ.get("GITHUB_TOKEN") is None:
        raise click.BadParameter("GITHUB_TOKEN not set.")


def create_github_repository(
    model_id: str, description: str, delete_existing: bool = False
) -> Repository:
    """
    Create a GitHub repository for the model.
    Args:
       model_id: The ID of the model.
       description: The description of the model.
       delete_existing: Delete the existing repository if it exists. (Will prompt you.)
    """
    check_github_token()
    org = github.get_organization("armadillo-ai")
    repos = org.get_repos()
    current_names = [repo.full_name for repo in repos]
    if f"armadillo-ai/{model_id}" in current_names:
        if not delete_existing:
            raise click.BadParameter(
                f"Model repository {model_id} already exists."
            )
        else:
            console.print(
                f"[red]:rotating_light: Model repository [bold]{model_id}[/bold] already exists, but you have opted to delete it.[/red]"
            )
            click.confirm("Are you sure you want to delete it?", abort=True)
            org.get_repo(model_id).delete()
            console.print(
                f":white_check_mark: Deleted remote repository [bold]{model_id}[/bold].",
                style="green",
            )
    created_repository = org.create_repo(
        name=model_id,
        description=description,
        private=True,
    )
    console.print(
        f":white_check_mark: Created {'[italic](new)[/italic] ' if delete_existing else ''}remote repository [bold]{model_id}[/bold]:",
        style="green",
    )
    console.print(f"   {created_repository.html_url}", style="blue")
    return created_repository
