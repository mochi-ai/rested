def min(limit):
    def validator(v, accept=None, reject=None):
        try:
            v = len(v)
        except TypeError:
            pass
        if v < limit: reject(f'expected_min_{limit}')
    return validator
min.dynamic = True
