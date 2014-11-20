from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from frontend.models import UserInfo


def loginUser(request):
    if request.method == 'GET':
        if request.user.is_authenticated() and request.user.is_active:
            return HttpResponseRedirect(reverse('frontend:foyer'))
        return render(request, 'frontend/login.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_active:
                    return HttpResponseRedirect(reverse('frontend:foyer'))
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
    if user.is_active:
        user.userinfo.name = request.POST['name']
        user.userinfo.gender = request.POST['gender']
        user.userinfo.department = request.POST['department']
        user.userinfo.studentClass = request.POST['studentClass']
    else:
        user.userinfo = UserInfo(
            name=request.POST['name'],
            gender=request.POST['gender'],
            department=request.POST['department'],
            studentClass=request.POST['studentClass'],
        )
        user.is_active = True
    user.userinfo.save()
    user.save()
    return HttpResponseRedirect(reverse('frontend:profile'))


@user_passes_test(lambda user: user.is_active)
def profile(request):
    return render(request, 'frontend/profile.html', {'user': request.user})


@user_passes_test(lambda user: user.is_active)
def foyer(request):
    return render(request, 'frontend/foyer.html', {'user': request.user,
        'sidebar_select': 0})


@user_passes_test(lambda user: user.is_active)
def message(request):
    return HttpResponse('message')


@user_passes_test(lambda user: user.is_active)
def resources(request):
    if request.method == 'GET':
        return render(request, 'frontend/resources.html', {'user':
            request.user, 'sidebar_select': 3, 'superuser':
            request.user.is_superuser})
    else:
        raise Http404


@user_passes_test(lambda user: user.is_superuser)
def manageResources(request):
    if request.method == 'GET':
        return render(request, 'frontend/manage/resources.html', {'user':
            request.user, 'sidebar_select': 3 })
    else:
        raise Http404


@user_passes_test(lambda user: user.is_active)
def scores(request):
    return render(request, 'frontend/scores.html', {'user': request.user,
        'sidebar_select': 2})


@user_passes_test(lambda user: user.is_active)
def competitions(request):
      return render(request, 'frontend/competitions.html', {'user':
          request.user, 'sidebar_select': 1})


@user_passes_test(lambda user: user.is_active)
def applyTeam(request):
    user = request.user
    user.is_applyingTeam = True
    user.userinfo.teamCategory = request.POST['teamCategory']
    user.userinfo.teamRole = request.POST['teamRole']
    user.userinfo.teamName = request.POST['teamName']
    user.userinfo.coach = request.POST['coach']
    user.userinfo.birth = request.POST['birth']
    user.userinfo.politicalBackground = request.POST['politicalBackground']
    user.userinfo.phoneNum = request.POST['phoneNum']
    user.userinfo.email = request.POST['email']
    user.userinfo.address = request.POST['address']
    user.userinfo.work = request.POST['work']
    return HttpResponseRedirect(reverse('frontend:profile'))


def userManagement(request):
    return render(request, 'frontend/userManagement.html', {'sidebar_select': 4})


def resourceManagement(request):
    return render(request, 'frontend/resourceManagement.html', {'sidebar_select': 5})


def scoreManagement(request):
    return render(request, 'frontend/scoreManagement.html', {'sidebar_select': 6})
