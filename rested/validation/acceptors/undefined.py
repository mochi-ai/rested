from ..utils import Undefined

def undefined(v, accept, reject=None):
    if v == Undefined: accept(v)
    return v
