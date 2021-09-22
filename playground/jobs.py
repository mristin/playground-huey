"""Specify longer-running jobs."""

import logging
import pathlib

import icontract
from huey import SqliteHuey

import playground.common

logging.basicConfig(level=logging.INFO)

CONFIG = playground.common.initialize_config()

HUEY = SqliteHuey(filename=str(CONFIG.huey_path))


@HUEY.task()  # type: ignore
@icontract.require(lambda project_id: playground.common.PROJECT_ID_RE.match(project_id))
def convert(uploaded_file_path: str, project_id: str) -> None:
    """Convert the file to the desired format."""
    logger = logging.getLogger("playground.jobs.convert")

    source_pth = pathlib.Path(uploaded_file_path)
    target_pth = CONFIG.converted_files_dir / project_id / source_pth.name
    tmp_pth = target_pth.parent / (target_pth.name + ".tmp")

    target_pth.parent.mkdir(exist_ok=True)
    try:
        logger.info("Starting to convert %s to: %s", source_pth, tmp_pth)
        text = source_pth.read_text()
        tmp_pth.write_text(text.upper())

        logger.info("Moving converted %s to: %s", tmp_pth, target_pth)
        tmp_pth.rename(target_pth)
        logger.info("Conversion finished: %s", target_pth)

        logger.info("Removing the uploaded file: %s", source_pth)
        source_pth.unlink()
        logger.info("The uploaded file has been removed: %s", source_pth)
    finally:
        tmp_pth.unlink(missing_ok=True)
