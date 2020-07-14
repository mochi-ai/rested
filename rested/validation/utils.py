import os
import importlib
from functools import wraps
from inspect import getmembers, isfunction


# class to represent a value that was undefined, this lets us differentiate between a passed null and non existant
class Undefined(): pass

# error class used to short circuit validation chain and accept a value
class ShortCircuit(Exception):

    def __init__(self, value):
        self.value = value
        super().__init__()

# validation error called when validation is rejected
class ValidationError(Exception):

    def __init__(self, code):
        self.code = code
        super().__init__(code)

# utility function to accept value
def accept(value):
    raise ShortCircuit(value)

# utility function to reject value
def reject(code):
    raise ValidationError(code)

# call validation function then return value
def passthrough(func):
    @wraps(func)
    def wrapped(value, *args, **kwargs):
        func(value, *args, **kwargs)
        return value
    return wrapped

# get a value in a nested dictionary
def dig(dictionary, keys):
    value = dictionary
    if not isinstance(keys, list):
        keys = [keys]
    for k in keys:
        if not isinstance(value, dict): raise KeyError(k)
        value = value[k]
    return value

# put a value in a nested dictionary, created dicts along path when missing
def place(dictionary, keys, value):
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value

# magic function to import and attach all validation functions from the specified directory
def attach(cls, dpth, dot):
    vdir = os.path.dirname(os.path.realpath(__file__)) + '/' + dpth
    tree = os.listdir(vdir)
    for path in tree:
        if path.startswith('_'): continue
        module = importlib.import_module(dot + "." + path[:-3])
        validators = getmembers(module, isfunction)
        for _, validator in validators:
            cls.attach(validator)


# check for extra keys in data given schema
# def extras(data, schema):
#     extra = set(data.keys()) - set(schema.keys())
#     for k in schema:
#         if type(schema.get(k)) is dict and type(data.get(k)) is dict:
#             extra.append(extras(data[k], schema[k]))
#     return extra
