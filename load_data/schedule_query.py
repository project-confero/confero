#!/usr/bin/env python
import os
import webbrowser

import click
from dotenv import load_dotenv
from google.cloud import bigquery_datatransfer_v1
from google.oauth2 import service_account


load_dotenv()

def get_query(query_file, year):
    with open(query_file) as file:
        sql = file.read().format(year=year)

    return sql

def get_gbq_creds(auth_creds):

    return service_account.Credentials.\
        from_service_account_file(
            auth_creds
        ).with_scopes(
            [
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/devstorage.read_only'
            ],
        )

AUTH_CREDS=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
PROJECT = os.getenv("PROJECT")
REGION = os.getenv("REGION")
QUERY_FILE = "sql/connections.sql"
PARENT = f"projects/{PROJECT}/locations/us"


@click.command()
@click.option('--year', default='20', help='2 digit year as string.')
def schedule_query(year):
    TRANSFER_CONFIG = {
        "display_name": f"Candidates and Connections for {year}",
        "data_source_id":"scheduled_query",
        "params":{
            "query": get_query(QUERY_FILE, year),
        },
        "schedule": "1 of month 07:00",
    }

    client = bigquery_datatransfer_v1.DataTransferServiceClient(
        credentials=get_gbq_creds(AUTH_CREDS)
    )
    transfer_config = bigquery_datatransfer_v1.TransferConfig(**TRANSFER_CONFIG)
    response = client.create_transfer_config(
        request={
                "parent": PARENT,
                "transfer_config": transfer_config,
            }
    )

    print("Created scheduled query '{}'".format(response.name))

if __name__ == "__main__":
    schedule_query()
