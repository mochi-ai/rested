from . import signals
from . import errors
from django.http import JsonResponse

urlpatterns = []
handler404 = errors.handler(404, 'Not Found')
handler500 = errors.handler(500, 'Server Error')
handler403 = errors.handler(403, 'Permission Denied')
handler400 = errors.handler(400, 'Bad Request')
handler_csrf = errors.handler(403, 'Permission Denied: CSRF Failure')

websocketpatterns = signals.patterns
