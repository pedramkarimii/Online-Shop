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
    sub_directories = [getattr(instance, field) for field in keys or []]
    return f"{root}/{'/'.join(sub_directories)}/{uuid4()}.{extension}"
