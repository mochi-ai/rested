def integer(v, accept=None, reject=None):
    if not isinstance(v, int): reject('expected_integer')
