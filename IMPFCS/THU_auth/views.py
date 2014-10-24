from django.http import HttpResponse, Http404
import json


def auth(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except KeyError:
        raise Http404
    if username.isdigit() and len(username) == 10:
        return HttpResponse(json.dumps({'valid': True}))
    else:
        return HttpResponse(json.dumps({'valid': False}))
