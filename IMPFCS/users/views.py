from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def test(request):
    return render(request, 'users/test.html', {})


def addUser(request):
    try:
        username = request.POST['username']
        pwd = request.POST['password']
        User.objects.create_user(username, password=pwd)
        return HttpResponseRedirect(reverse('users:test'))
    except (KeyError, ):
        raise Http404

def removeUser(request):
    username = request.POST['username']
    user = get_object_or_404(User, username=username)
    user.delete()
    return HttpResponseRedirect(reverse('users:test'))


def userLogin(request):
    return HttpResponse('This is userLogin')


def userLogout(request):
    return HttpResponse('This is userLogout')