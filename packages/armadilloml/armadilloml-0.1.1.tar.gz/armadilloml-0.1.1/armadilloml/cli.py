import os
import subprocess
import shutil
import docker
import rich_click as click
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from typing import Optional
from armadilloml.templating import (
    render_template_directory,
    render_template_file,
)
from .utils import (
    get_armadillo_value,
    require_armadillo_project,
    set_armadillo_value,
    validate_id,
)

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
    path = os.path.join(os.getcwd(), path)
    validate_id(id)
    if os.path.exists(path):
        if delete:
            print(
                f"[red] :warning: Deleting [bold]{path}[/bold] :warning: [/red]"
            )
            shutil.rmtree(path)
        else:
            raise click.BadParameter("Path already exists")
    os.mkdir(path)
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
    render_template_directory
    print(
        f"[green] :white_check_mark: Successfully created [bold]{path}[/bold] :white_check_mark: [/green]"
    )


@click.command()
def build():
    """
    Run the build process for an Armadillo model.

    The build process has a few steps:
    1. Populates the .build directory with a Dockerfile.
    2. Builds the Docker image.
    3. Pushes the Docker image to the Google Cloud Registry.
    3. Runs the image on Google Cloud.
    4. Updates the model object in Armadillo's database.
    """
    require_armadillo_project()
    if os.path.isdir(".build"):
        shutil.rmtree(".build")
    shutil.copytree(os.getcwd(), ".build")
    render_template_file("templates/Dockerfile.template", ".build/Dockerfile")
    render_template_file(
        "templates/.dockerignore.template", ".build/.dockerignore"
    )
    id_ = get_armadillo_value("id")
    client = docker.from_env()
    with console.status(
        f"[blue]Building model [bold]{id_}...[/blue]", spinner_style="blue"
    ) as status:
        tag = f"armadilloml-{id_}"
        result, _ = client.images.build(path=".build", tag=tag)
    # client.images.get(tag).tag(tag=f"gcr.io/armadillo-ml/{tag}")
    set_armadillo_value("dockerImageId", result.id)
    set_armadillo_value("dockerImageTag", tag)
    console.log(
        f"[green]:white_check_mark: Successfully built model: [bold]{id_}[/bold]. [/green]"
    )
    console.log(
        "[blue]Run [bold]armadilloml deploy[/bold] to deploy the model.[/blue]"
    )


@click.command()
def deploy():
    """
    Upload the model to Google Cloud Run.
    """
    require_armadillo_project()
    if not os.path.isdir(".build"):
        raise click.BadParameter("No .build directory found.")
    docker_image = get_armadillo_value("dockerImageId")
    docker_tag = get_armadillo_value("dockerImageTag")
    id_ = get_armadillo_value("id")
    os.system("gcloud config set run/region us-east1")
    p = subprocess.run(
        f"gcloud run deploy --source .build",
        text=True,
        shell=True,
        stdout=subprocess.PIPE,
        # input=id_,
    )
    # os.system(f"gcloud run deploy --source .build | test")


@click.group(help="The CLI for managing your ML models.")
def cli():
    """
    Reference for the command line interface. (This is referenced in poetry.toml)
    """
    pass


cli.add_command(login)
cli.add_command(init)
cli.add_command(build)
cli.add_command(deploy)
