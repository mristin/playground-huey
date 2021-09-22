"""Provide common patterns and structures for the playground."""
import os
import pathlib
import re
from typing import List

PROJECT_ID_RE = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$")


class Config:
    """Represent shared config between the backend and the jobs."""

    def __init__(self) -> None:
        """Initialize with the default values."""
        self.port = 8000
        self.host = "0.0.0.0"
        self.uploaded_files_dir = (
            pathlib.Path(os.path.realpath(__file__)).parent.parent
            / "runtime_data"
            / "uploaded_files"
        )
        self.converted_files_dir = (
            pathlib.Path(os.path.realpath(__file__)).parent.parent
            / "runtime_data"
            / "converted_files"
        )
        self.huey_path = (
            pathlib.Path(os.path.realpath(__file__)).parent.parent
            / "runtime_data"
            / "huey.sqlite"
        )


def initialize_config() -> Config:
    """
    Load the configuration and perform a series of checks.

    The checks aim not to be complete, but to capture the most obvious run-time errors.

    :raise: :class:`RuntimeError` if the configuration is not valid
    """
    config = Config()

    errors = []  # type: List[str]

    if not config.uploaded_files_dir.exists():
        errors.append(
            f"Uploaded files directory does not exist: {config.uploaded_files_dir}"
        )
    else:
        if not config.uploaded_files_dir.is_dir():
            errors.append(
                f"Expected uploaded files directory to be a directory, "
                f"but it is not: {config.uploaded_files_dir}"
            )

    if not config.converted_files_dir.exists():
        errors.append(
            f"Converted files directory does not exist: {config.converted_files_dir}"
        )
    else:
        if not config.converted_files_dir.is_dir():
            errors.append(
                f"Expected converted files directory to be a directory, "
                f"but it is not: {config.converted_files_dir}"
            )

    if not config.huey_path.exists():
        if not config.huey_path.parent.exists():
            errors.append(
                f"Parent directory of the Huey database does not exist: "
                f"{config.huey_path.parent}"
            )
        else:
            if not config.huey_path.parent.is_dir():
                errors.append(
                    f"Expected the parent of the Huey database to be a directory, "
                    f"but it is not: {config.huey_path.parent}"
                )
    else:
        if not config.huey_path.is_file():
            errors.append(
                f"Expected the Huey path to be a file, but it is not: "
                f"{config.huey_path}"
            )

    if len(errors) > 0:
        bullets = "\n".join("* {error}" for error in errors)
        raise RuntimeError(f"The configuration is invalid:\n{bullets}")

    return config
