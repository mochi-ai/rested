def boolean(v, accept=None, reject=None):
    if not isinstance(v, bool): reject('expected_boolean')
