"""Call a backend endpoint to test it."""

import os
import pathlib

import requests


def main() -> None:
    """Execute the main routine."""
    url = "http://127.0.0.1:8000/convert/"

    this_dir = pathlib.Path(os.path.realpath(__file__)).parent
    test_file_pth = this_dir.parent / "test_data" / "testme.txt"

    with test_file_pth.open("rb") as fid:
        with requests.post(
            url, files={"file": fid}, data={"project_id": "bimprove"}
        ) as resp:
            print(f"Response was: {resp.status_code} {resp.text}")


if __name__ == "__main__":
    main()
