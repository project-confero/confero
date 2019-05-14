def _get_names_data(file_path):
    """Get names data from a text file"""

    lines = []
    names = []
    with open(file_path) as file:
        for index, line in enumerate(file.readlines()):
            lines.append(line.strip('\n').split(','))
            for name in line.split(','):
                names.append([name.strip('\n'), index])
        names.sort()

        return names, lines


# Export the names data, so we only have to parse the file once.
NAMES_DATA = _get_names_data('./fec/data/names.txt')
