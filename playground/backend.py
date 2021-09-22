"""Provide a playground conversion of file."""
import logging
import sys
import uuid

import aiofiles
import uvicorn
from fastapi import FastAPI, Form, UploadFile, File, HTTPException

import playground.common
import playground.jobs

CONFIG = playground.common.initialize_config()

logging.basicConfig(level=logging.INFO)


APP = FastAPI(title="FastAPI ⟷ Huey playground", description=__doc__, version="1.0.0")


@APP.post("/convert/", response_model=str)
async def convert(
    project_id: str = Form(
        ...,
        description="Project ID that the file is associated with",
        max_length=1024,
        regex=playground.common.PROJECT_ID_RE.pattern,
    ),
    file: UploadFile = File(..., description="File to be converted"),
) -> str:
    """Convert the supplied file."""
    logger = logging.getLogger("playground.backend.convert")

    target_pth = CONFIG.uploaded_files_dir / f"{file.filename}.{uuid.uuid4()}"
    tmp_pth = target_pth.parent / (target_pth.name + ".tmp")

    # We perform a manual two-phase commit:
    # 1) Store the file on disk
    # 2) Publish the path and the meta-data to Huey
    #
    # If something goes wrong *before* we published to Huey, we should unroll
    # the conversion.

    sent_to_huey = False

    max_size = 30 * 1024 * 1024 * 1024

    try:
        logger.info(
            "Storing the file %s of project %s to: %s",
            file.filename,
            project_id,
            tmp_pth,
        )

        async with aiofiles.open(tmp_pth, "wb") as fid:
            size = 0
            while content := await file.read(32 * 1024):
                await fid.write(content)

                size += len(content)
                if size > max_size:
                    raise HTTPException(
                        413,
                        f"The file is too large. Max size: {max_size} bytes, "
                        f"received so far: {size}",
                    )

        logger.info("Moving %s to: %s", tmp_pth, target_pth)

        tmp_pth.rename(target_pth)

        logger.info("Sending for conversion: %s", target_pth)

        playground.jobs.convert(
            uploaded_file_path=str(target_pth), project_id=project_id
        )

        sent_to_huey = True
        logger.info("Sent for conversion: %s", target_pth)
    finally:
        tmp_pth.unlink(missing_ok=True)

        # See the remark regarding the two-phase commit above
        if not sent_to_huey:
            target_pth.unlink(missing_ok=True)

    return "File has been queued for conversion."


def main() -> int:
    """Run the server."""
    logger = logging.getLogger("playground.backend.main")

    logger.info("Starting the service on: %s:%d", CONFIG.host, CONFIG.port)
    # noinspection PyTypeChecker
    uvicorn.run(APP, host=CONFIG.host, port=CONFIG.port)

    return 0


if __name__ == "__main__":
    sys.exit(main())
