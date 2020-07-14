from json import loads, JSONDecodeError

def json(v, accept=None, reject=None):
    try:
        return loads(v)
    except JSONDecodeError:
        reject(f'expected_json_object')
