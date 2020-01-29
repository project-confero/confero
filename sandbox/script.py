# %%
from functools import partial
import os
import pkg_resources

from dotenv import load_dotenv, find_dotenv
from nameparser import HumanName
import pandas as pd
import pandas_gbq
import psycopg2
from tqdm.auto import tqdm

load_dotenv(find_dotenv())

TEMP_FILE = '/tmp/sql.csv'
DIR = f'{os.getcwd()}/sandbox'

CONFIG = {
    "candidates": {
        "table":
        "fec_candidate",
        "filename":
        "sql/candidates.sql",
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
        ["id", "name", "party", "office", "state", "district"],
        "index":
        "id"
    },
    "committees": {
        "table":
        "fec_committee",
        "filename":
        "sql/committees.sql",
        "csv_columns": [
            "id", "candidate_id", "committee_id", "committee_type",
            "committee_designation"
        ],
        "csv_types": {},
        "table_columns": ["candidate_id", "committee_id"],
        "index":
        "id"
    },
    "contributions": {
        "table": "fec_contribution",
        "filename": "sql/contributions.sql",
        "csv_columns":
        ["committee_id", "name", "zip_code", "transaction_amount"],
        "csv_types": {
            "committee_id": "str",
            "name": "str",
            "zip_code": "str",
            "transaction_amount": "float",
        },
        "table_columns": ["committee_id", "name", "zip", "transaction_amount"],
        "index": None
    },
}

CANDIDATE_CONFIG = CONFIG["candidates"]
COMMITTEE_CONFIG = CONFIG["committees"]
CONTRIBUTION_CONFIG = CONFIG["contributions"]


def get_names_data():
    resource_package = __name__
    resource_path = '/'.join(('data', 'names.txt'))
    path_to_names = pkg_resources.resource_filename(resource_package,
                                                    resource_path)

    lines = []
    names = []

    with open(path_to_names) as file:
        for index, line in enumerate(file.readlines()):
            lines.append(line.strip('\n').split(','))
            for name in line.split(','):
                names.append([name.strip('\n'), index])
        names.sort()

    return names, lines


def get_nicknames(name, names, lines):
    # Search for all names that match first_name
    all_names = nickname_search(name, names)

    names = [name] + [
        lines[all_names[index][1]][0] for index, _ in enumerate(all_names)
    ] if all_names is not None else [name]

    return names


def nickname_search(first_name, names):
    """ Find and return the index of key in sequence names  for first_name"""
    lb = 0
    ub = len(names)

    while True:
        if lb == ub:  # If region of interest (ROI) becomes empty
            return None
        # Next probe should be in the middle of the ROI
        mid_index = (lb + ub) // 2
        # Fetch the item at that position
        item_at_mid = names[mid_index][0]
        # How does the probed item compare to the target?
        if item_at_mid == first_name:
            upper_mid_index = mid_index
            lower_mid_index = mid_index
            while names[upper_mid_index + 1][0] == first_name:
                upper_mid_index = upper_mid_index + 1
            while names[lower_mid_index - 1][0] == first_name:
                lower_mid_index = lower_mid_index - 1
            return names[lower_mid_index:upper_mid_index + 1]  # Found it!
        if item_at_mid < first_name:
            lb = mid_index + 1  # Use upper half of ROI next time
        else:
            ub = mid_index  # Use lower half of ROI next time


def get_conn():
    db_prefix = 'RDS_' if 'RDS_DB_NAME' in os.environ else 'DB_'

    return psycopg2.connect(
        dbname=os.getenv(db_prefix + 'DB_DB_NAME', 'confero'),
        user=os.getenv(db_prefix + 'USERNAME', 'postgres'),
        password=os.getenv(db_prefix + 'PASSWORD', 'postgres'),
        host=os.getenv(db_prefix + 'HOSTNAME', 'localhost'),
        port=os.getenv(db_prefix + 'PORT', '5432'),
    )


def read_csv(config):
    filename = config["filename"]
    data_types = config["csv_types"]
    with open(f"{DIR}/{filename}") as file:
        return pandas_gbq.read_gbq(
            file.read(),
            index_col=config["index"],
        ).drop_duplicates().astype(data_types)


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


def clean_field(field):
    sc = set("~!@#$%^&*()_+/?,<>.'`~\"")
    return ''.join([c for c in field if c not in sc])


def find_matches(df, names, lines, row):

    nick_names = get_nicknames(row['first'], names, lines)

    index = pd.MultiIndex.from_tuples(
        [(f, row.middle, row.last, row.zip_code) for f in nick_names],
        names=['first', 'middle', 'last', 'zip_code'])

    all_possible_matches = pd.Series(
        [row.index for _ in range(len(nick_names))], index=index, name='id')

    df_join = df.join(all_possible_matches, how='inner')

    return ''.join(df_join.id.to_list())


if __name__ == '__main__':

    candidates = read_csv(CANDIDATE_CONFIG)
    committees = read_csv(COMMITTEE_CONFIG)
    contributions = read_csv(CONTRIBUTION_CONFIG)

    tqdm.pandas('rows processed: ')
    contributions['parsed_name'] = contributions['name'].progress_apply(
        lambda x: HumanName(x).as_dict())
    for col in ['first', 'middle', 'last']:
        contributions[col] = contributions['parsed_name'].progress_apply(
            lambda x: clean_field(x[col]))  # noqa
        contributions[col] = contributions[col].str.upper()

    GROUPBY_COLS = ['first', 'middle', 'last', 'zip_code', 'committee_id']
    contributions = contributions.\
        groupby(GROUPBY_COLS).sum().\
        reset_index()

    names, lines = get_names_data()
    matches = partial(find_matches, contributions, names, lines)
    contributions['match_id'] = contributions.progress_apply(matches, axis=1)

    print(contributions.groupby(['match_id']).count().shape)
