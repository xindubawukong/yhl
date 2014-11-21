# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from frontend.models import UserInfo
from django.contrib.auth.models import User
import datetime
import mongo

client = mongo.MongoClient()


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
                return render(request, 'frontend/login.html', {'errorMsg' : u'学号或密码错误'})
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
    resources = client.get_resource('resource')
    for i in range(len(resources)):
            resources[i]['id'] = str(resources[i]['_id'])
    if request.user.is_superuser:
        applications = client.get_application('application')
        app = []
        for i in range(len(applications)):
            applications[i]['id'] = str(applications[i]['_id'])
            if applications[i]['state'] == 'suspending':
                app.append(applications[i])
        teamApplications = client.get_teamApplication('teamApplication')
        teamApp = []
        for i in range(len(teamApplications)):
            teamApplications[i]['id'] = str(teamApplications[i]['_id'])
            if teamApplications[i]['state'] == 'suspending':
                teamApp.append(teamApplications[i]) 
        return render(request, 'frontend/adminFoyer.html', 
            {
                'user': request.user,
                'resources': resources, 
                'applications': app,
                'teamApplications': teamApp,
                'sidebar_select': 0})
    else:
        applications = client.get_user_application('application', request.user.username)
        app = []
        for i in range(len(applications)):
            app.append(applications[i])
            app[-1]['loc'] = client.get_resource_by_id('resource', app[-1]['resource_id'])['loc']
        teamApplications = {'teamApplications': [{'teamName': u'游泳队', 'year': 2014, 'month': 1, 'day': 1, 'state': 'rejected'}]}
        resourceApplications = {'resourceApplications': [{'loc': 'loc1', 'date': '20140102', 'state': 'accpeted'}]}
        return render(request, 'frontend/foyer.html', 
            {   'user': request.user,
                'teamApplications': teamApplications['teamApplications'], 
                'resourceApplications': app,
                'resources': resources, 
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


@user_passes_test(lambda user: user.is_active)
def scores(request):
    scores = {'scores': [{'category': '射击', 'name': '奥运会', 'competition': '男子50米步枪3X40', 'rank': '1', 'score': '80', 'time': '0.01s', 'dist': '2m', 'state': 'rejected'}]}
    return render(request, 'frontend/scores.html', 
        {   'user': request.user,
            'scores': scores['scores'],
            'sidebar_select': 2
        })


@user_passes_test(lambda user: user.is_active)
def competitions(request):
      return render(request, 'frontend/competitions.html', {'user':
          request.user, 'sidebar_select': 1})


@user_passes_test(lambda user: user.is_active)
def applyTeam(request):
    user = request.user
    user.userinfo.is_applyingTeam = True
    user.userinfo.teamCategory = request.POST['teamCategory']
    user.userinfo.teamRole = request.POST['teamRole']
    user.userinfo.teamName = request.POST['teamName']
    user.userinfo.coach = request.POST['coach']
    user.userinfo.birth = request.POST['birth']
    user.userinfo.politicalBackground = request.POST['politicalBackground']
    user.userinfo.phoneNum = request.POST['phoneNum']
    user.email = request.POST['email']
    user.userinfo.address = request.POST['address']
    user.userinfo.work = request.POST['work']
    user.userinfo.applyTeamTime = datetime.datetime.now()
    user.userinfo.save()
    user.save()
    client.insert_teamApplication('teamApplication', {
        "s_id" : request.user.username,
        "teamName" : request.POST['teamCategory'],
        "date" : str(datetime.datetime.now())[:10],
        "state" : 'suspending' # rejected \ suspending
    })
    return HttpResponseRedirect(reverse('frontend:profile'))


@user_passes_test(lambda user: user.is_superuser)
def management(request):
    if request.method == 'GET':
        return render(request, 'frontend/management.html', {'user':
            request.user, 'sidebar_select': 4 })
    else:
        raise Http404


def addResource(request):
    client.insert_resource('resource', 
        {
            'loc': request.POST['loc'],
            'date': request.POST['date'],
            'desc': request.POST['desc']
        })
    return HttpResponseRedirect(reverse('frontend:foyer'))


def applyResource(request, resource_id):
    client.insert_application('application', {
    "s_id" : request.user.username,
    "resource_id" : resource_id,
    "date" : str(datetime.datetime.now())[:10],
    "state" : 'suspending' # rejected \ suspending
    })
    return HttpResponseRedirect(reverse('frontend:foyer'))


def replyResourceApplication(request, reply, application_id):
    assert reply in ['accept', 'reject']
    client.change_application_state('application', reply + 'ed', application_id)
    return HttpResponseRedirect(reverse('frontend:foyer'))


def replyTeamApplication(request, reply, application_id):
    assert reply in ['accept', 'reject']
    client.change_teamApplication_state('teamApplication', reply + 'ed', application_id)
    app = client.get_teamApplication_by_id('teamApplication', application_id)
    user = User.objects.get(username=app['s_id'])
    if reply == 'accept':
        user.userinfo.is_teamMember = True
    user.userinfo.is_applyingTeam = False
    user.userinfo.save()
    user.save()
    return HttpResponseRedirect(reverse('frontend:foyer'))