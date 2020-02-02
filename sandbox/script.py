# %%
import pandas as pd
import psycopg2
import os
import sys

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

YEAR = sys.argv[1]

print(f'Generating data for {YEAR}')

TEMP_FILE = '/tmp/sql.csv'
DIR = f'{os.getcwd()}/sandbox'
JSON_DIR = f'{os.getcwd()}/confero-front/public/data/{YEAR}'

CONFIG = {
    "candidates": {
        "table":
        "fec_candidate",
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
        "fec_committee",
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
        "fec_contribution",
        "filename":
        "itcont.txt",
        "csv_columns": [
            "committee_id", "amendment_indicator", "report_type",
            "primary_general_indicator", "image_number", "transaction_type",
            "entity_type", "name", "city", "state", "zip", "employer",
            "occupation", "transaction_date", "transaction_amount", "other_id",
            "transaction_id", "file_number", "memo_code", "memo_text", "id"
        ],
        "csv_types": {
            "committee_id": "str",
            "amendment_indicator": "str",
            "report_type": "str",
            "primary_general_indicator": "str",
            "image_number": "str",
            "transaction_type": "str",
            "entity_type": "str",
            "name": "str",
            "city": "str",
            "state": "str",
            "zip": "str",
            "employer": "str",
            "occupation": "str",
            # "transaction_date": "datetime64",
            "transaction_amount": "int",
            "other_id": "str",
            "transaction_id": "str",
            "file_number": "str",
            "memo_code": "str",
            "memo_text": "str",
            "id": "int"
        },
        "table_columns": [
            "id", "committee_id", "name", "zip", "employer", "occupation",
            "transaction_amount"
        ]
    },
}

CANDIDATE_CONFIG = CONFIG["candidates"]
COMMITTEE_CONFIG = CONFIG["committees"]
CONTRIBUTION_CONFIG = CONFIG["contributions"]


def get_conn():
    db_prefix = 'RDS_' if 'RDS_DB_NAME' in os.environ else 'DB_'

    return psycopg2.connect(
        dbname=os.getenv(db_prefix + 'DB_DB_NAME', 'sandbox'),
        user=os.getenv(db_prefix + 'USERNAME', 'postgres'),
        password=os.getenv(db_prefix + 'PASSWORD', 'postgres'),
        host=os.getenv(db_prefix + 'HOSTNAME', 'localhost'),
        port=os.getenv(db_prefix + 'PORT', '5432'),
    )


def read_csv(config, skiprows=None, nrows=None):
    filename = config["filename"]
    headers = config["csv_columns"]
    data_types = config["csv_types"]

    return pd.read_csv(
        f"{DIR}/data/{YEAR}/{filename}",
        header=None,
        sep="|",
        names=headers,
        dtype=data_types,
        index_col="id",
        skiprows=skiprows,
        nrows=nrows,
        error_bad_lines=False,
        warn_bad_lines=True,
        # No quoting, to avoid an issue with an unclosed quote
        quoting=3,
    ).drop_duplicates()


def without_id(columns):
    copy = columns[:]

    if "id" in copy:
        copy.remove("id")

    return copy


def pluck_csv(csv, config):
    columns = config["table_columns"]
    return csv[without_id(columns)]


def save_csv_to_load(csv, config):
    columns = config["table_columns"]
    index = "id" in columns

    csv.to_csv(TEMP_FILE, header=False, index=index)


def table_to_pandas(table, select="*"):
    with get_conn() as conn:
        return pd.read_sql_query(f'select {select} from {table}', con=conn)


def query_to_pandas(filename):
    with get_conn() as conn:
        sql = open(f"{DIR}/sql/{filename}", "r").read()
        return pd.read_sql_query(sql, con=conn)


def clear_table(table):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE {table} CASCADE;")


def load_csv_to_table(config):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            table = config["table"]
            columns = config["table_columns"]

            file = open(TEMP_FILE, "r")
            # Clear table
            cursor.execute(f"TRUNCATE {table} CASCADE;")
            # Load new data
            column_string = ",".join(columns)
            cursor.copy_expert(
                f"copy {table} ({column_string}) from STDIN CSV QUOTE '\"'",
                file)


def send_to_db(csv, config):
    data = pluck_csv(csv, config)
    save_csv_to_load(data, config)
    load_csv_to_table(config)


def run_sql_file(filename):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            sql = open(f"{DIR}/sql/{filename}", "r").read()
            cursor.execute(sql)


def run_sql_query(filename):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            sql = open(f"{DIR}/sql/{filename}", "r").read()
            cursor.execute(sql)

            print(f"===records from {filename}===")

            for record in cursor:
                print(record)


def download_sql_query(sql_file, save_file):
    with get_conn() as conn:
        with conn.cursor() as cursor:
            sql = open(f"{DIR}/sql/{sql_file}", "r").read()
            file = open(f"{DIR}/data/{save_file}", "w")

            cursor.copy_expert(
                f"copy ({sql}) TO STDOUT WITH CSV HEADER",
                file,
            )


def clean_field(data, field):
    data[field] = data[field].str.replace('[^a-zA-Z0-9]', '')
    return data


def candidates_to_json():
    filename = f"{JSON_DIR}/candidates.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as file:
        candidates = query_to_pandas("connected_candidates.sql")
        candidates.to_json(file, "records")


def connections_to_json():
    filename = f"{JSON_DIR}/connections.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as file:
        connections = table_to_pandas("fec_connection",
                                      "score, source_id, target_id")
        connections.to_json(file, "records")

def parties_to_json(candidates):
    parties = query_to_pandas("partisionship_score.sql")
    parties["candidates"] = candidates[party].count()


    filename = f"{JSON_DIR}/parties.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)



# %%
if __name__ == '__main__':
    # %%
    print("reading CSVs")
    candidates = read_csv(CANDIDATE_CONFIG)
    committees = read_csv(COMMITTEE_CONFIG)
    contributions = read_csv(CONTRIBUTION_CONFIG)

    # %%
    print("cleaning committees")
    print("committees", len(committees))
    # Primary committee only
    committees = committees[committees['committee_designation'].isin(
        ['P', 'A', 'D'])]
    print("committees (primary)", len(committees))
    # Future work: why so many?
    committees = committees.drop_duplicates(subset="committee_id")
    print("committees deduped", len(committees))
    # Removes committees without candidates
    committees = committees[committees['candidate_id'].isin(candidates.index)]
    print("committees with candidates", len(committees))

    # %%
    print("cleaning contributions")

    clean_field(contributions, "employer")
    clean_field(contributions, "occupation")

    # FUTURE WORK: Other valid types?
    # See: https://www.fec.gov/campaign-finance-data/transaction-type-code-descriptions
    contributions = contributions[(contributions.transaction_type == "15")
                                  | (contributions.transaction_type == "15E")]

    # FUTURE WORK: ActBlue earmarks
    actblue = contributions[contributions['committee_id'] == 'C00401224']
    actblue_clean = actblue[actblue['memo_text'].str.find('REFUND') == -1]
    if len(actblue_clean) > 0:
        actblue_clean['committee_id'] = actblue_clean['memo_text'].str.extract(
            r'(C[0-9]{8})')
        contributions = contributions.append(actblue_clean)

    contributions = contributions[contributions['committee_id'] != 'C00401224']

    print("contributions", len(contributions))
    contributions = contributions[contributions['committee_id'].isin(
        committees.committee_id)]
    print("contributions with committees", len(contributions))

    # %%
    print("sending to db")
    send_to_db(candidates, CANDIDATE_CONFIG)
    # %%
    send_to_db(committees, COMMITTEE_CONFIG)
    # %%
    send_to_db(contributions, CONTRIBUTION_CONFIG)

    print("making connections")

    # %%
    clear_table("fec_connection")
    run_sql_file("make_connections.sql")

    print("writing JSON")

    # Output connections for frontent
    connections_to_json()
    candidates_to_json()

    print("done")
