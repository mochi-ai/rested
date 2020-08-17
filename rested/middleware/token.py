from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password


# user mixin for token authentication
class TokenUserMixin(models.Model):
    token = models.CharField(max_length=128, null=True)

    class Meta:
        abstract = True

    def assign_token(self):
        length = 48
        allowed_chars = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        if self.id is None: raise RuntimeError('User must have an id assigned before token can be generated.')
        token = str(self.id) + ':' + get_random_string(length, allowed_chars)
        self.set_token(token)
        return token

    def set_token(self, raw_token):
        self.token = make_password(raw_token)
        self._token = raw_token

    def check_token(self, raw_token):
        if not self.token: return False
        def setter(raw_token):
            self.set_token(raw_token)
            self._token = None
            self.save(update_fields=["token"])
        return check_password(raw_token, self.token, setter)

# token authentication middleware
class TokenAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.authenticate(request)
        return self.get_response(request)

    @classmethod
    def authenticate(cls, request):
        creds = cls.get_token(request)
        if not creds or ':' not in creds: return
        id, _ = creds.split(':', 1)
        user = get_user_model().objects.filter(id=id).first()
        if not user.check_token(creds): return
        request.csrf_processing_done = True
        request.user = user

    @staticmethod
    def get_token(request):
        return str(request.META.get('HTTP_X_API_KEY', '')).strip()
