import os
import json
import rich_click as click


def validate_id(model_id: str):
    """Validates that the ID contains no spaces or special characters."""
    if not model_id:
        raise click.BadParameter("ID cannot be empty")
    if " " in model_id:
        raise click.BadParameter("ID cannot contain spaces")
    return model_id


def require_armadillo_project():
    """
    Checks that the current directory is an Armadillo project.
    """
    if not os.path.exists("armadillo.json"):
        raise click.BadParameter("Not in an Armadillo project")


def set_armadillo_value(key: str, value: str):
    """
    Saves a value to armadillo.json.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    data[key] = value
    with open("armadillo.json", "w") as f:
        json.dump(data, f, indent=4)


def get_armadillo_value(key: str):
    """
    Gets a value from armadillo.json.
    """
    with open("armadillo.json") as f:
        data = json.load(f)
    return data[key]
