from functools import wraps


def passes_test(test_func, code, message):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            return (code, {'error': message})
        return wrapped
    return decorator


def public(func):
    return func

def authenticated(func):
    message = 'User must be authenticated to access this resource'
    return passes_test(lambda r: r.user.is_authenticated, 401, message)(func)

def admin(func):
    message = 'You do not have permission to access this resource'
    return authenticated(passes_test(lambda r: r.user.is_superuser, 403, message)(func))

def staff(func):
    message = 'You do not have permission to access this resource'
    return authenticated(passes_test(lambda r: r.user.is_staff or r.user.is_superuser, 403, message)(func))
