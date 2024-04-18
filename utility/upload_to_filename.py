from django.db import models
from uuid import uuid4


def maker(root: str, instance, filename: str, keys: list | None = None):
    """Generates a unique file path for saving files.

    Args:
        root (str): The root directory where the file will be saved.
        instance: The instance associated with the file.
        filename (str): The original filename of the file.
        keys (list | None): A list of attribute names to create sub-directories within the root directory.
                            Defaults to None.

    Returns:
        str: The generated unique file path.
    """
    filename, extension = filename.split(".")
    sub_directories = []
    if keys:
        for key in keys:
            if hasattr(instance, key):
                value = getattr(instance, key)
                if isinstance(value, models.Model):
                    sub_directories.append(str(value))
                else:
                    sub_directories.append(str(value))
    return f"{root}/{'/'.join(sub_directories)}/{uuid4()}.{extension}"
