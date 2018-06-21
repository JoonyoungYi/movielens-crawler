import re


def get_query(name):
    m = re.search('^(?P<l>.*), (?P<r>[0-9a-zA-Z]+)$', name)
    if m:
        return m.group('r') + ' ' + m.group('l')
    else:
        return name
