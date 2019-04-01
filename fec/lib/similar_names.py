from fec.lib.names_data import NAMES_DATA

SUFFIXES = [
    ' SR',
    ' JR',
    ' II',
    ' III',
    ' IV',
    ' MD',
]
PREFIXES = [
    ' DR',
    ' MR',
    ' MRS',
    ' MS',
]
PUNCTUATION = [
    '.',
]


def _string_clean(string_to_fix):
    for fix in PREFIXES + SUFFIXES + PUNCTUATION:
        string_to_fix = string_to_fix.replace(fix, '')

    return string_to_fix


def _first_names(full_name):
    return _string_clean(full_name.split(',')[1]).split()


def _last_name(full_name):
    return _string_clean(full_name.split(',')[0])


def _get_nicknames(name):
    names, lines = NAMES_DATA

    # Search for all names that match first_name
    all_names = _nickname_search(name, names)

    if all_names is None:
        return [name]

    names = [
        lines[all_names[index][1]][0] for index, _ in enumerate(all_names)
    ]

    return names


def _nickname_search(first_name, names):
    """ Find and return the index of key in sequence names  for first_name"""
    first_name = first_name.lower()
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


def _regex_list(list_of_elements, optional=False, punctuation=None):
    q_mark = ''
    if optional:
        q_mark = '?'
    if punctuation:
        all_ps = ''.join(['(%s)?' % p for p in punctuation])
        for index, element in enumerate(list_of_elements):
            list_of_elements[index] = element + all_ps

    return '(%s)%s' % ('|'.join(list_of_elements), q_mark)


def _regex_affixes():
    regex_suffixes = _regex_list(
        SUFFIXES.copy(), optional=True, punctuation=PUNCTUATION)
    regex_prefixes = _regex_list(
        PREFIXES.copy(), optional=True, punctuation=PUNCTUATION)

    return regex_prefixes, regex_suffixes


def regex_name(full_name):
    """
    Return the regex to search for names that are
    probably the same as the user's name
    """
    prefixes, suffixes = _regex_affixes()
    affixes = prefixes + suffixes

    rest_of_first = []

    try:
        first_name, *rest_of_first = _first_names(full_name)
    except IndexError:
        return full_name

    return prefixes + _last_name(full_name) + affixes + ', ' + \
        _regex_list(_get_nicknames(first_name)).upper() + \
        _regex_list(rest_of_first, optional=True) + affixes
