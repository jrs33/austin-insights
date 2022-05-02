"""CLI interface for project_name project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
from sodapy import Socrata
import boto3
import json
import os


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m project_name` and `$ project_name `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
    backfill_issued_permits_to_s3()

def backfill_issued_permits_to_s3():

    scraper = Socrata(os.environ.get("ODP_URL"), os.environ.get("ODP_API_TOKEN"))

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_KEY")
    )
    s3_bucket = s3_client.Bucket(os.environ.get("S3_BUCKET_NAME"))

    result_generator = scraper.get_all("3syk-w9eu", limit=1)

    for item in result_generator:
        project_id = item.get("project_id")
        key = 'permits/2022/5/1/' + project_id + ".json" # remove date hard code
        data = json.dumps(item)
        s3_bucket.put_object(Key=key, Body=data)