from distutils.util import strtobool

def boolean(v, accept=None, reject=None):
    if isinstance(v, str): return bool(strtobool(v))
    return bool(v)
