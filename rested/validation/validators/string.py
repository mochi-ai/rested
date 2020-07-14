def string(v, accept=None, reject=None):
    if not isinstance(v, str): reject('expected_string')
