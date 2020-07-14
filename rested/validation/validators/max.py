def max(limit):
    def validator(v, accept=None, reject=None):
        try:
            v = len(v)
        except TypeError:
            pass
        if v > limit: reject(f'expected_max_{limit}')
    return validator
max.dynamic = True
