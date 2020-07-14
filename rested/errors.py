from django.http import JsonResponse


class AbortException(Exception):
    def __init__(self, status, data):
        self.status = status
        self.data = data

def abort(status, data=None):
    if not data: data = {}
    raise AbortException(status, data)

def handler(status, message, data=None):
    def handler(request, exception=None, reason=None):
        return JsonResponse(data={
            'status': status,
            'message': message,
            'data': data if data is not None else {}
        }, status=status)
    return handler
