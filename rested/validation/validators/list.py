lst = type([])
def list(v, accept=None, reject=None):
    if not isinstance(v, lst): reject('expected_list')
