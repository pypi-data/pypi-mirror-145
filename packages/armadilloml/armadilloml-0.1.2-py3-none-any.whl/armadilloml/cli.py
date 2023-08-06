import os
import shutil
import rich_click as click
from git import Repo
from rich.console import Console
from rich.prompt import Prompt
from typing import Optional
from .github import create_github_repository
from .utils import validate_id
from .templating import render_template_directory

console = Console()


@click.command()
def login():
    """Login to Armadillo"""
    # TODO Implement this for real.
    api_key = Prompt.ask("Enter your Armadillo API key")
    return


@click.command()
@click.argument("path", type=click.Path(), default=None)
@click.option(
    "--id",
    type=str,
    help="The ID of the model to create.",
    prompt="Model ID",
)
@click.option(
    "--name",
    type=str,
    help="The name of the model to create.",
    prompt="Model Name",
)
@click.option(
    "--delete",
    "-d",
    type=bool,
    default=False,
    flag_value=True,
    help="Delete the directory if it already exists.",
)
def init(path: Optional[str], id: str, name: str, delete: bool):
    """
    Initializes the directory structure for a new model.
    """
    remote_repo = create_github_repository(id, name, delete)
    path = os.path.join(os.getcwd(), path)
    validate_id(id)
    if os.path.exists(path):
        if delete:
            console.print(
                f":rotating_light: Deleting local directory [bold]{path}[/bold]",
                style="red",
            )
            shutil.rmtree(path)
        else:
            raise click.BadParameter("Path already exists")
    # os.mkdir(path)
    repo = Repo.clone_from(remote_repo.clone_url, path)
    render_template_directory(
        "templates/project-template/",
        path,
        {
            "model_id": id,
            "model_name": name,
            "name": "Max Davish",  # TODO Get Armadillo username for real
            "email": "davish9@gmail.com",  # TODO Get Armadillo email for real
        },
    )
    console.print(
        f":white_check_mark: Successfully created [bold]{path}[/bold]",
        style="green",
    )
    open_in_vscode = click.confirm("Open in VS Code?", abort=False)
    if open_in_vscode:
        os.system(f"code {path}")


@click.group(help="The CLI for managing your ML models.")
def cli():
    """
    Reference for the command line interface. (This is referenced in poetry.toml)
    """
    pass


cli.add_command(login)
cli.add_command(init)
