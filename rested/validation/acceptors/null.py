def null(v, accept, reject=None):
    if v is None: accept(v)
    return v
