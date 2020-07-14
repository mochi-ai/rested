import json as sjson
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile

class RestedJSONEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, FieldFile):
            try:
                return o.url
            except ValueError:
                return ''
        return super().default(o)

def dumps(*args, **kwargs):
    kwargs['cls'] = kwargs.get('cls', RestedJSONEncoder)
    return sjson.dumps(*args, **kwargs)

def loads(*args, **kwargs):
    return sjson.loads(*args, **kwargs)
