def nonempty(v, accept=None, reject=None):
    if len(v) == 0: reject(f'expected_nonempty')
