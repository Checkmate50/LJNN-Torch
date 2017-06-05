"""
A python file with some helpful functions for extracting data defined for importing

Written by @Checkmate
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
    b = b.copy()
    for key in a.keys():
        if not b.has_key(key):
            b[key] = a[key]
    return b

