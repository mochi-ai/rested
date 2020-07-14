def member(collection):
    def validator(v, accept=None, reject=None):
        if v not in collection: reject(f'expected_set_membership')
    return validator
member.dynamic = True
