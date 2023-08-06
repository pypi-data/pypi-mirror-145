"""
This file provides utilities for creating files based on templates in this 
library. The reason we need this is so that we can create a starter Armadillo
project on the developer's local machine, while interpolating some values
like the name of the project.
"""

import os
import pkg_resources


def render_template_file(
    template_file: str, destination_file: str, template_args: dict = None
):
    """
    Copies a template file to the destination file.
    Arguments:
        template_file: The path to the template file.   (str)
        destination_file: The path to the destination file. (str)
        template_args: A dictionary of arguments to pass to the template. (dict)
    """
    resource_package = __name__
    template = pkg_resources.resource_string(
        resource_package, template_file
    ).decode("utf-8")
    if template_args:
        for template_key, template_value in template_args.items():
            template = template.replace(
                f"{{{{{template_key}}}}}", template_value
            )
    with open(destination_file, "w") as f:
        f.write(template)


def render_template_directory(
    template_directory: str,
    destination_directory: str,
    template_args: dict = None,
):
    """
    Copies an entire template directory to a destination directory while
    applying any templating argumetns.
    """
    ## Get all of the files in the template directory
    template_files = pkg_resources.resource_listdir(
        __name__, template_directory
    )
    template_files = [
        f
        for f in template_files
        if not (pkg_resources.resource_isdir(__name__, f))
    ]
    for template_file in template_files:
        render_template_file(
            template_file=os.path.join(template_directory, template_file),
            destination_file=os.path.join(
                destination_directory, template_file
            ),
            template_args=template_args,
        )
    return True
