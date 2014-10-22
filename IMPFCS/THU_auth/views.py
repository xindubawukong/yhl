from django.http import HttpResponse, Http404
import json


def auth(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404
    if username.startswith('valid'):
        return HttpResponse(json.dumps({'valid': True}))
    else:
        return HttpResponse(json.dumps({'valid': False}))
