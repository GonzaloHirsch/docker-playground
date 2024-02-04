import uuid
import requests
import json
from functools import reduce

import os

import logging
logging.basicConfig(level=logging.DEBUG)


def get_files(protocol: str, host: str, path: str, port: str):
    r = requests.get(f'{protocol}://{host}:{port}{path}')
    return json.loads(r.text)


def reduce_files(accum: dict, file_data: str):
    accum["lower"] += sum(1 for c in file_data if c.islower())
    accum["upper"] += sum(1 for c in file_data if c.isupper())
    accum["num"] += sum(1 for c in file_data if c >= "0" and c <= "9")
    accum["space"] += sum(1 for c in file_data if c == " ")
    return accum


def main(uid: str, protocol: str, host: str, path: str, port: str):
    files_left = True

    stats = {
        "lower": 0,
        "upper": 0,
        "num": 0,
        "space": 0
    }

    # Iterate while there are files to be parsed
    while files_left:
        data = get_files(protocol, host, path, port)

        # Expect data for the files
        if data["status"] != "ok":
            files_left = False
            break

        reduce(reduce_files, data["data"], stats)

    logging.info(f"Stopping consumer process id={uid}...")
    logging.info(f"Stats are: {stats}")


if __name__ == "__main__":
    uid = uuid.uuid4().hex
    logging.info(f"Starting consumer process id={uid}...")
    main(uid=uid, protocol=os.getenv("APP_PRODUCER_PROTOCOL"), host=os.getenv(
        "APP_PRODUCER_HOST"), path=os.getenv("APP_PRODUCER_PATH"), port=os.getenv("APP_PRODUCER_PORT"))
