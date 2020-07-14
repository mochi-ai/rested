def json(v, accept=None, reject=None):
    if isinstance(v, dict):
        return v
    reject(f'expected_json_object')
