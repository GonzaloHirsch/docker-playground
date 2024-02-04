import threading
from typing import Union
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from aiofiles import open

import os
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG)

# Must import threading to ensure the file lock is happening

# Declraing a lock
lock = threading.Lock()

file_count = 1
file_limit = 0

app = FastAPI()
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
).instrument(app)

# Get any configs from the environment
APP_BATCH_SIZE = int(os.getenv("APP_BATCH_SIZE"))
APP_FILE_LOCATION = os.getenv("FILE_LOCATION")
file_limit = int(os.getenv("APP_FILE_COUNT"))

# Get the app start time
start_time = datetime.now()


@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)


@app.get("/")
def get_root():
    return {"status": "ok", "uptime_seconds": (datetime.now() - start_time).total_seconds()}


async def read_file(filepath: str) -> str:
    async with open(filepath, mode='r') as f:
        contents = await f.read()
    return contents


@app.get("/files")
async def get_files():
    global file_count, file_limit
    logging.info("Handling file request...")
    lock.acquire()
    # Ensure there are files to read
    if file_count > file_limit:
        # Must release lock before returning
        lock.release()
        return {"status": "error", "data": "no more files"}

    # Keep a copy of the file count to be read from
    file_read_start = int(file_count)

    # Update the file count
    file_count += APP_BATCH_SIZE

    # Release the lock for other processes to continue handling the requests
    lock.release()

    # Read all the files based on the thread copy of the variable
    files = [await read_file(f"{APP_FILE_LOCATION}/{i}") for i in range(file_read_start, file_read_start + APP_BATCH_SIZE)]
    logging.info("Returning file information...")

    # Return the data with the files
    return {"status": "ok", "data": files}
