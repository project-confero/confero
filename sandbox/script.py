#%%
import pandas as pd
import psycopg2
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

TEMP_FILE = "/tmp/sql.csv"
DIR = f"{os.getcwd()}/sandbox"

CONFIG = {
    "candidates": {
        "table":
        "candidate",
        "filename":
        "cn.txt",
        "csv_columns": [
            "id", "name", "party", "election_year", "state", "office",
            "district", "incumbent_challenger_status", "status",
            "principal_committee_id", "address_state_1", "address_state_2",
            "address_city", "address_state", "address_zip"
        ],
        "csv_types": {
            "district": "str"
        },
        "table_columns":
        ["id", "name", "party", "office", "state", "district"]
    },
    "committees": {
        "table":
        "committee",
        "filename":
        "ccl.txt",
        "csv_columns": [
            "candidate_id", "candidate_election_year", "fec_election_year",
            "committee_id", "committee_type", "committee_designation", "id"
        ],
        "csv_types": {},
        "table_columns": ["candidate_id", "committee_id"]
    },
    "contributions": {
        "table":
        "contribution",
        "filename":
        "by_date/itcont_2020_20190629_20190930.txt",
        "csv_columns": [
            "committee_id", "amendment_indicator", "report_type",
            "primary_general_indicator", "image_number", "transaction_type",
            "entity_type", "name", "city", "state", "zip", "employer",
            "occupation", "transaction_date", "transaction_amount", "other_id",
            "transaction_id", "file_number", "memo_code", "memo_text", "id"
        ],
        "csv_types": {},
        "table_columns":
        ["id", "committee_id", "name", "zip", "employer", "occupation"]
    },
}

CANDIDATE_CONFIG = CONFIG["candidates"]
COMMITTEE_CONFIG = CONFIG["committees"]
CONTRIBUTION_CONFIG = CONFIG["contributions"]


def get_conn():
    db_prefix = 'RDS_' if 'RDS_DB_NAME' in os.environ else 'DB_'

    return psycopg2.connect(
        dbname=os.getenv(db_prefix + 'DB_SANDBOX_DB_NAME', 'confero_sandbox'),
        user=os.getenv(db_prefix + 'USERNAME', 'postgres'),
        password=os.getenv(db_prefix + 'PASSWORD', 'postgres'),
        host=os.getenv(db_prefix + 'HOSTNAME', 'localhost'),
        port=os.getenv(db_prefix + 'PORT', '5432'),
    )


def read_csv(config):
    filename = config["filename"]
    headers = config["csv_columns"]
    data_types = config["csv_types"]

    return pd.read_csv(
        f"{DIR}/data/{filename}",
        header=None,
        sep="|",
        names=headers,
        dtype=data_types,
        index_col="id",
    ).drop_duplicates()


def without_id(columns):
    copy = columns[:]

    if "id" in copy:
        copy.remove("id")

    return copy


def pluck_csv(csv, config):
    columns = config["table_columns"]
    return csv[without_id(columns)]


def save_csv_to_load(csv):
    csv.to_csv(TEMP_FILE, header=False)


def load_csv_to_table(config):
    conn = get_conn()
    cursor = conn.cursor()

    table = config["table"]
    columns = config["table_columns"]

    file = open(TEMP_FILE, "r")
    # Clear table
    cursor.execute(f"TRUNCATE {table};")
    # Load new data
    # cursor.copy_from(file, table, sep=",", columns=columns)
    # TODO: columns. Handle no ID?
    cursor.copy_expert(f"copy {table} from STDIN CSV QUOTE '\"'", file)
    cursor.execute("commit;")

    conn.close()


def send_to_db(csv, config):

    data = pluck_csv(csv, config)
    save_csv_to_load(data)
    load_csv_to_table(cursor, config)


#%%
candidates = read_csv(CANDIDATE_CONFIG)

#%%
committees = read_csv(COMMITTEE_CONFIG)

#%%
contributions = read_csv(CONTRIBUTION_CONFIG)

#%%
send_to_db(cursor, candidates, CANDIDATE_CONFIG)
#%%
send_to_db(cursor, committees, COMMITTEE_CONFIG)
#%%
send_to_db(cursor, contributions, CONTRIBUTION_CONFIG)
