import os
from functools import partial
import pkg_resources
import sys
import pandas_gbq
import pandas as pd
import numpy as np

import recordlinkage as rl
from recordlinkage.base import BaseIndexAlgorithm
from recordlinkage.preprocessing import clean

TEMP_FILE = '/tmp/sql.csv'
DIR = f'{os.getcwd()}/sandbox'
YEAR = sys.argv[1]
NAMES_PATH = pkg_resources.resource_filename(__name__, '/'.join(('data',
                                                                 'names.txt')))
GROUPBY_COLS = ['first', 'middle', 'last', 'zip_code', 'id']
MATCH_COLS = ['first', 'middle', 'last', 'zip_code']
CANDIDATE_COLUMNS = [
    "id", "name", "office", "party", "state", "district", "score",
    "contribution_count", "contribution_amount"
]
CONTRIBUTION_CONFIG = {
    "filename": "sql/contributions.sql",
    "csv_types": {
        "id": "str",
        "first": "str",
        "middle": "str",
        "last": "str",
        "zip_code": "str",
        "transaction_amount": "float",
    },
    "index": None
}


def listify(x):
    """Make a list of the argument if it is not a list."""

    if isinstance(x, list):
        return x

    if isinstance(x, tuple):
        return list(x)

    if x is None:
        return []

    return [x]


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

    return set(names)


def validate_name(name):
    return name if isistance(name, str) and pd.notna(name) else ''


class NickNameIndex(BaseIndexAlgorithm):
    """Custom class for indexing"""

    def __init__(self, left_on=None, right_on=None, missing_value=True):
        super(NickNameIndex, self).__init__()
        self.missing_value = missing_value
        self.left_on = left_on
        self.right_on = right_on

    def _get_left_and_right_on(self):
        if self.right_on is None:
            return (self.left_on, self.left_on)

        return (self.left_on, self.right_on)

    def _link_index(self, df_a, df_b):
        left_on, right_on = self._get_left_and_right_on()

        left_on = listify(left_on)
        right_on = listify(right_on)

        blocking_keys = ["blocking_key_%d" % i for i, v in enumerate(left_on)]

        names, lines = get_names_data('sandbox/data/names.txt')
        nicknames = partial(get_nicknames, names, lines)

        # make a dataset for the data on the left
        data_left = pd.DataFrame(df_a[left_on], copy=False)
        data_left.columns = blocking_keys
        data_left['index_x'] = np.arange(len(df_a))
        # add rows for each nickname
        nicknames_left = pd.DataFrame.from_records(
            data_left[blocking_keys[0]].apply(validate_name).apply(
                nicknames).tolist()).stack().reset_index(
                    level=1, drop=True).rename(blocking_keys[0])
        data_left = data_left.drop(blocking_keys[0], axis=1).\
            join(nicknames_left).reset_index(drop=True)

        # make a dataset for the data on the right
        data_right = pd.DataFrame(df_b[right_on], copy=False)
        data_right.columns = blocking_keys
        data_right['index_y'] = np.arange(len(df_b))

        # merge the dataframes
        pairs_df = data_left.merge(data_right, how='inner', on=blocking_keys)
        if not self.missing_value:
            pairs_df.dropna(subset=blocking_keys, inplace=True)
        return pd.MultiIndex(
            levels=[df_a.index.values, df_b.index.values],
            codes=[pairs_df['index_x'].values, pairs_df['index_y'].values],
            verify_integrity=False)


def get_matches(df, first_name, middle_name, last_name, zip_code):
    indexer = rl.Index()
    indexer.add([
        NickNameIndex(
            left_on=[first_name, middle_name, last_name, zip_code],
            missing_value=False),
    ])
    links = indexer.index(df)

    # transform
    cl = rl.Compare()
    cl.exact(zip_code, zip_code, label='zip_code')
    features = cl.compute(links, df)

    return features


def read_csv(config, year):
    filename = config["filename"]
    data_types = config["csv_types"]
    with open(f"{DIR}/{filename}") as file:
        return pandas_gbq.read_gbq(
            file.read().format(year=year),
            index_col=config["index"],
        ).drop_duplicates().astype(data_types)


if __name__ == '__main__':
    contr = read_csv(CONTRIBUTION_CONFIG, YEAR)
    contr['contribution_count'] = 1
    # Clean
    for col in ['first', 'last', 'middle']:
        contr[col] = clean(contr[col])
    contributions = contr.groupby(GROUPBY_COLS).sum().reset_index()

    # match records
    features = get_matches(contributions,
                           *['first', 'middle', 'last', 'zip_code'])

    contributions['new_index'] = contributions.index
    dupes = features.index.get_level_values(0).values
    matches = features.index.get_level_values(1).values
    contributions.loc[matches, 'new_index'] = dupes
    contributions.reset_index(inplace=True)
    contributions.set_index('new_index', inplace=True)

    multi_contr = contributions[contributions.index.duplicated()][[
        'id', 'transaction_amount'
    ]]
    multi_contr_j = multi_contr.join(
        multi_contr, lsuffix='_source', rsuffix='_target')
    multi_contr_j = multi_contr_j[
        multi_contr_j['id_source'] != multi_contr_j['id_target']]

    connections = multi_contr_j.pivot_table(
        index=['id_target', 'id_source'], aggfunc='count')
    connections = connections[connections['transaction_amount_source'] > 2]
    connections.reset_index(inplace=True)
    connections.rename(
        columns={
            'id_target': 'target_id',
            'id_source': 'source_id',
            'transaction_amount_source': 'score'
        },
        inplace=True)
    connections[['source_id', 'target_id', 'score']].\
        to_json(
            f'confero-front/public/data/20{YEAR}/connections.json',
            orient='records'
    )
    contr.groupby([
        "id",
        "name",
        "office",
        "party",
        "state",
        "district"]
    ).sum()[
            ['transaction_amount', "contribution_count"]
        ].reset_index().set_index('id').\
    join(
            connections.groupby('source_id').sum()[['score']],
            how='inner'
        ).\
        rename(
            columns={'transaction_amount': 'contribution_amount'}
        ).\
        sort_values('score', ascending=False).\
        to_json(
            f'confero-front/public/data/20{YEAR}/candidates.json',
            orient='records'
        )
