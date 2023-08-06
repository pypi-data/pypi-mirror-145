import re
import string
import uuid
from collections import namedtuple


def escape_literal(literal):
    literal = literal.replace("'", "''")
    return f"'{literal}'"


def escape_identifier(identifier):
    identifier = identifier.replace('"', '""')
    return f'"{identifier}"'


def extract_column_names(obj):
    if isinstance(obj, dict):
        columns = list(obj.keys())
    elif isinstance(obj, namedtuple):
        columns = list(obj._fields)
    else:
        columns = None

    return columns


def column_name_generator():
    len_letters = len(string.ascii_lowercase)
    i = 0
    while True:
        letter = string.ascii_lowercase[i % len_letters]
        column_name = letter * (1 + i // len_letters)
        yield column_name
        i += 1


def format_namedtuple_names(names):
    formatted_names = []
    seen_names = set()
    for i, name in enumerate(names):
        name = re.sub('[^0-9a-zA-Z_]', '_', name)
        # Namedtuple name can not start with a number of underscore
        if re.match('[0-9_]', name[0]):
            name = 'c' + name
        # Add underscores until the name is unique
        while name in seen_names:
            name = name + '_'

        seen_names.add(name)
        formatted_names.append(name)

    return formatted_names


def is_namedtuple(obj):
    return isinstance(obj, tuple) \
           and hasattr(obj, '_asdict') \
           and hasattr(obj, '_fields')


def make_random_table_name():
    return f't{uuid.uuid4().hex}'


def normalize_data(data):
    if hasattr(data, 'itertuples'):
        # Pandas
        data = data.to_dict('records')

    return data
