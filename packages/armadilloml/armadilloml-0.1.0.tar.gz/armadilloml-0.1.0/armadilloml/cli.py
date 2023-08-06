from typing import DefaultDict
import rich_click as click
import os
import json
from rich import print
from rich.prompt import Prompt
from typing import Optional

def validate_id(model_id: str):
    """Validates that the ID contains no spaces or special characters."""
    if not model_id:
        raise click.BadParameter('ID cannot be empty')
    if ' ' in model_id:
        raise click.BadParameter('ID cannot contain spaces')
    if not model_id.isalnum():
        raise click.BadParameter('ID cannot contain special characters')
    return model_id

def create_armadillo_json(model_id: str, model_name: str) -> dict: 
    """Creates the empty armadillo.json file"""
    return {
        "id": model_id,
        "name": model_name,
        "scripts": {
            "add": "poetry add",
            "build": "armadillo build",
            "deploy": "armadillo deploy"
        }
    }

@click.command()
def login():
    """Login to Armadillo"""
    # TODO Implement this for real.
    api_key = Prompt.ask("Enter your Armadillo API key:")
    return
    
    
@click.command()
@click.argument('path', type=click.Path(exists=False), nargs=1)
@click.argument('--name',)
@click.argument('--id',)
def init(path: str, name: Optional[str], id: Optional[str]):
    """
    Initializes a new Armadillo project. The armadillo project contains the
    following files:
    - armadillo.json
    - pypoetry.toml
    - main.py
    """
    path = path if path else os.getcwd()
    full_path = os.path.expanduser(path)
    print(full_path)
    return 
    validate_id(model_id)
    armadillo_json = create_armadillo_json(model_id, name)
    with open(os.path.join(full_path, 'armadillo.json'), 'w') as f:
        json.dump(armadillo_json, f, indent=4)

@click.command() 
def build():
    """
    Run the build process for an Armadillo model.
    
    The build process has a few steps:
    1. Populates the .build directory with a Dockerfile. 
    2. Builds the Docker image.
    3. Runs the image on Google Cloud. 
    4. Updates the model object in Armadillo's database. 
    """
    
@click.group(help="The CLI for managing your ML models.")
def cli():
    """
    Reference for the command line interface. (This is referenced in poetry.toml)
    """
    pass

cli.add_command(login)
cli.add_command(init)
cli.add_command(build)
