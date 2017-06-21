"""
A python file with some helpful functions for extracting data defined for importing

Written by Dietrich Geisler
"""


def get_data(filename, expected = [], defaults = dict()):
    """
    Given a string filename,
    A list of data lines we expect to obtain,
    And a list of defaults
    Extract the file names to call from the given file
    And returns the constructed dictionary
    """
    
    data = defaults
    with open(filename, "r") as f:
        for line in f:
            sline = line[:line.find("#")].strip().split()
            if len(sline) < 2:
                continue
            data[sline[0]] = map(reduce_type, sline[1:])
            if len(data[sline[0]]) == 1:
                data[sline[0]] = data[sline[0]][0]
    for expect in expected:
        if not data.has_key(expect):
            raise ValueError("Expected the " + expect + " data value")
    return data


def reduce_type(item):
    """
    Given a list of strings 'item'
    Return that string as its most basic type
    """
    if (item.lower() == "true"):
        return True
    if (item.lower() == "false"):
        return False
    if (item[0] == "-" and item[1:].isdigit()) or item.isdigit():
        return int(item)
    try:
        return float(item)
    except(ValueError):
        return item

    
def combine_dicts(a, b):
    to_return = a.copy()
    for key in b.keys():
        if not to_return.has_key(key):
            to_return[key] = b[key]
    return to_return

# Text colors from https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
def print_info(s):
    print('\033[92m' + str(s) + '\033[0m')

def print_warning(s):
    print('\033[93m' + str(s) + '\033[0m')

def print_error(s):
    print('\033[91m' + str(s) + '\033[0m')
