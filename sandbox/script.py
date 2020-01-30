# %%
import os
from functools import partial
import pkg_resources

import pandas_gbq
from tqdm.auto import tqdm

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
            "first": "str",
            "middle": "str",
            "last": "str",
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


def get_names_data(file_path):

    lines = []
    names = []

    with open(file_path) as file:
        for index, line in enumerate(file.readlines()):
            lines.append(line.strip('\n').split(','))
            for name in line.split(','):
                names.append([name.strip('\n'), index])
        names.sort()

    return names, lines


def get_nicknames(names, lines, name):
    # Search for all names that match first_name
    all_names = nickname_search(name, names)

    names = [
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


def read_csv(config):
    filename = config["filename"]
    data_types = config["csv_types"]
    with open(f"{DIR}/{filename}") as file:
        return pandas_gbq.read_gbq(
            file.read(),
            index_col=config["index"],
        ).drop_duplicates().astype(data_types)


def clean_field(field):
    sc = set("~!@#$%^&*()_-={}[]|+/?,<>.'`~\"1234567890")
    return ''.join([c for c in field if c not in sc])


def find_matches(df, names, lines, row):
    last_name = row['last']
    df_match = df.query("(last == @last_name")
    if df_match.shape[0] == 1:
        return None

    df_match = df_match[df_match['zip_code'] == row['zip_code']]
    if df_match.shape[0] == 1:
        return None

    nick_names = get_nicknames(names, lines, row['first'])
    df_match = df_match[[x in nick_names for x in df_match['first']]]
    if df_match.shape[0] == 1:
        return None

    if row['middle']:
        middle_names = [row['middle'], None]
    if len(row['middle']) > 1:
        middle_names += [row['middle'][0]]
    else:
        middle_names = [None]
    df_match = df_match[[x in middle_names for x in df_match['middle']]]
    if df_match.shape[0] == 1:
        return None

    return ''.join([str(x) for x in df_match.index])


if __name__ == '__main__':
    path_to_names = pkg_resources.resource_filename(
        __name__, '/'.join(('data', 'names.txt')))

    # Extract
    # candidates = read_csv(CANDIDATE_CONFIG)
    # committees = read_csv(COMMITTEE_CONFIG)
    contributions = read_csv(CONTRIBUTION_CONFIG)

    # Clean
    tqdm.pandas('rows processed')
    for col in ['first', 'middle', 'last']:
        contributions[col] = contributions[col].progress_apply(clean_field)

    GROUPBY_COLS = ['first', 'middle', 'last', 'zip_code', 'committee_id']
    contributions = contributions.\
        groupby(GROUPBY_COLS).sum().\
        reset_index()

    # Transform
    names, lines = get_names_data(path_to_names)
    nick_names = partial(find_matches, contributions, names, lines)
    contributions['match_id'] = contributions.progress_apply(
        nick_names, axis=1)

    # print(contributions.groupby(['match_id']).count().shape)
