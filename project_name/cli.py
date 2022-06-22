import os
from datetime import datetime

import boto3
import requests
from dotenv import load_dotenv

PERMITS_CSV_FILE_URL = "https://data.austintexas.gov/api/views/3syk-w9eu/rows.csv?accessType=DOWNLOAD"


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m project_name` and `$ project_name `.
    """
    load_dotenv()
    backfill_issued_permits_to_s3()


def backfill_issued_permits_to_s3():
    print("downloading permit data...")
    with requests.get(PERMITS_CSV_FILE_URL, stream=True) as permits_download:
        with open(os.path.join(os.getcwd(), "permits.csv"), "w+") as local_csv:
            for chunk in permits_download.iter_content(chunk_size=1024):
                if chunk:
                    local_csv.write(chunk.decode("utf-8"))

    print("uploading to s3...")
    s3 = boto3.client("s3")
    current_time = datetime.now()
    object_name = "permits/{year}/{month}/{day}/permits.csv".format(
        year=current_time.year, month=current_time.month, day=current_time.day
    )
    s3.upload_file(
        os.path.join(os.getcwd(), "permits.csv"),
        os.environ.get("S3_BUCKET_NAME"),
        object_name,
    )

    print("done!")
