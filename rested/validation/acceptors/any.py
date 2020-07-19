def any(collection):
    def validator(v, accept, reject=None):
        if v in collection: accept(v)
        return v
    return validator
any.dynamic = True
