def nonnull(v, accept=None, reject=None):
    if v is None: reject('expected_nonnull')
