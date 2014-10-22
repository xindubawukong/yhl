from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from frontend.models import BasicInfo


def loginUser(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('frontend:profile'))
        return render(request, 'frontend/login.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_active:
                    return HttpResponseRedirect(reverse('frontend:profile'))
                else:  
                    return render(request, 'frontend/completeInfo.html', {'user' : user})
            else:
                return render(request, 'frontend/login.html', {'errorMsg' : 'Invalid username or password.'})
        except KeyError:
            raise Http404
    else:
        pass
    return HttpResponse('Try to login with:\n username=%s, password=%s' % (username, password))


def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('frontend:login'))


def completeInfo(request):
    user = request.user
    user.basicinfo = BasicInfo(name=request.POST['name'], gender=BasicInfo.MALE if request.POST['gender'] == 'male' else BasicInfo.FEMALE)
    user.basicinfo.save()
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('frontend:profile'))


@user_passes_test(lambda user: user.is_active)
def profile(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/admin/')
    return render(request, 'frontend/profile.html', {'user': request.user})
