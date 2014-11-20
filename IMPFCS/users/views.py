from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from frontend.models import UserInfo
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test


def _json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")


@user_passes_test(lambda user: user.is_superuser)
def listApplications(request):
    """
    list all team Member applications, sorted by ctime.
    returns {'applications': [{
        'studentNum',
        'name',
        'department',
        'studentClass',
        'teamCategory',
        'teamName',
        'teamRole',
        'coach',
        'ctime'}, ...]}
    """
    applicants = [appinfo.user for appinfo in UserInfo.objects.filter(is_applyingTeam=True)]
    ret = {'applications': [{
    'studentNum': applicant.username, 
    'name': applicant.userinfo.name,
    'department': applicant.userinfo.department,
    'studentClass': applicant.userinfo.studentClass,
    'teamCategory': applicant.userinfo.teamCategory,
    'teamName': applicant.userinfo.teamName,
    'teamRole': applicant.userinfo.teamRole,
    'coach': applicant.userinfo.coach,
    'ctime': str(applicant.userinfo.applyTeamTime).split('.')[0]
,
    } for applicant in applicants] }
    return _json_response(ret)


def teamMemberAccept(request):
    studentNum = request.POST['studentNum']
    try:
        user = User.objects.get(username=studentNum)
    except ObjectDoesNotExist:
        return _json_response({'success': 0, 'studentNum': studentNum})
    user.userinfo.is_applyingTeam = False
    user.userinfo.is_teamMember = True
    user.userinfo.save()
    user.save()
    return _json_response({'success': 1, 'studentNum': studentNum})


def teamMemberReject(request):
    studentNum = request.POST['studentNum']
    try:
        user = User.objects.get(username=studentNum)
    except ObjectDoesNotExist:
        return _json_response({'success': 0, 'studentNum': studentNum})
    user.userinfo.is_applyingTeam = False
    user.userinfo.is_teamMember = False
    user.userinfo.save()
    user.save()
    return _json_response({'success': 1, 'studentNum': studentNum})
