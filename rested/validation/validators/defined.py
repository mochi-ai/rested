from ..utils import Undefined

def defined(v, accept=None, reject=None):
    if v == Undefined:
        reject('expected_defined')
