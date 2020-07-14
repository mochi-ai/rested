from django.http import JsonResponse, HttpResponse
from rested import abort, validate, check, v
from .models import Person


def get(request):
    return {"payload": "get"}

def post(request):
    return {"payload": "post"}

def put(request):
    return {"payload": "put"}

def delete(request):
    return {"payload": "delete"}

def people_get(request, id):
    person = Person.objects.filter(id=id).first()
    if not person: abort(404)
    return person

def people_index(request):
    return Person.objects.all()

def boom(request):
    abort(400, {"payload": "boom"})
    return {"payload": "fizzle"}

def bang(request):
    abort(400)
    return {"payload": "fizzle"}

def kaboom(request):
    raise Exception('Kaboom!')

def status(request):
    return (444, {})

def unwrapped_http(request):
    return HttpResponse("hello")

def unwrapped_json(request):
    return JsonResponse({"route": "get"})

def index(request):
    return HttpResponse("Hello.")

def echo_params(request):
    return request.params

def echo_data(request):
    return request.data

def dupe(request, count=0):
    return {"payload": count}

def insecure(request):
    return ['a', 'b']

def csrf(request):
    return {}

@validate({
    "a": v.am,
    "b": {
        "c": v.am,
        "d": v.am,
    }
})
def vecho(request):
    return request.data

@validate({
    "age": v.am.string.to.integer
}, field="params")
def vquery(request):
    return request.params

def vpurl(request, num):
    errors, data = check({'num': num}, {'num': v.am.integer.to.string})
    return data
