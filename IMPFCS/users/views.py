from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
import json


def test(request):
    return render(request, 'users/test.html', {})


def addUser(request):
    try:
        username = request.POST['username']
        pwd = request.POST['password']
        User.objects.create_user(username, password=pwd)
        ret = json.dumps({'error': False})
    except (KeyError, ValueError):
        ret = json.dumps({'error': True, 'errorMsg': 'username or password unavailable'})
    except IntegrityError:
        ret = json.dumps({'error': True, 'errorMsg': 'Exist user with the same username'})
    return HttpResponse(ret)


def userLogin(request):
    try:
        username = request.POST['username']
        pwd = request.POST['password']
    except KeyError:
        ret = json.dumps({'error': True, 'errorMsg': 'username or password unavailable'})
        return HttpResponse(ret)

    user = authenticate(username=username, password=pwd)

    if user is not None:
        if user.is_active:
            login(request, user)
            ret = json.dumps({'error': False})
        else:
            ret = json.dumps({'error': True, 'errorMsg': 'inactive user'})
    else:
        ret = json.dumps({'error': True, 'errorMsg': 'illegal username or password'})
    
    return HttpResponse(ret)


def userLogout(request):
    return HttpResponse('This is userLogout')