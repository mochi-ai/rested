from functools import partial, reduce
from django.urls.conf import _path
from django.urls.resolvers import RoutePattern, RegexPattern
import re


# factory method that creates a pattern and tags it with a method
def factory(pattern, method):
    def wrapper(*args, **kwargs):
        p = pattern(*args, **kwargs)
        p.method = method
        return p
    return wrapper

# create a rest route scoped by method
def rest(route, method, view, decorators=None, kwargs=None, name=None, pattern='route'):

    # accept a decorator or list of decorators
    if not decorators: decorators = []
    if not isinstance(decorators, (list, tuple)): decorators = [decorators]

    # wrap view with decorators, decorators are applied right to left (bottom to top)
    for decorator in reversed(decorators):
        view = decorator(view)

    # proxy path function
    Pattern = RoutePattern if pattern == 'route' else RegexPattern
    return _path(route, view, kwargs=kwargs, name=name, Pattern=factory(Pattern, method))
