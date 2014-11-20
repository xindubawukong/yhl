from django.shortcuts import render
from django.http import Http404, HttpResponse

import time
import json
import re
import models

datesPattern = re.compile(r'^(\d\d\d\d\-\d\d\-\d\d;)*\d\d\d\d\-\d\d\-\d\d')

def _json_response(data):
    return HttpResponse(json.dumps(data), content_type="application/json")

def _check_superuser(user):
    return (user is not None) and (user.is_superuser)

def _check_active(user):
    return (user is not None) and (user.is_active)

def addScore(request):
    """
    the api of adding scores.
    POST takes resource name, description and dates(passed as a string
    "yyyy-MM-dd;yyyy-MM-dd;...", represents the dates of this resource) as
    arguments, and returns {'success': 1, 'resource_id'} or
    {'error': reason}.
    """
    if request.method == 'POST':
        user = request.user
        if not _check_superuser(request.user):
            return _json_response({'error': 'Permission denied'})
        category = request.POST['category']
        name = request.POST['name']
        competition = request.POST['competition']
        rank = request.POST['rank']
        score = request.POST['score']
        time = request.POST['time']
        distance = request.POST['distance']
        if (category is None) or (name is None) or (competition is None) or (rank is None) or (
                score is None) or (time is None) or (distance is None):
            return _json_response({'error': 'Missing necessary fields'})
        score_id = models.addScore(name, description, dates)
        return _json_response({
            'success': 1,
            'score_id': score_id.__str__()
            })
    else:
        raise Http404


def cancelResource(request):
    """
    the api of cancel Resources
    POST takes resource_id as argument, and returns
    {'success': 1, 'resource_id'} or {'error': reason}.
    """
    if request.method == 'POST':
        if not _check_superuser(request.user):
            return _json_response({'error': 'Permission denied'})
        resource_id = request.POST['resource_id']
        if (resource_id is None) or (resource_id.strip() == ''):
            return _json_response({'error': 'Missing necessary fields'})
        res = models.cancelResource(resource_id)
        if res['success']:
            return _json_response({'success': 1, 'resource_id':resource_id})
        else:
            return _json_response({'error': res['reason']})
    else:
        raise Http404

def cancelResourceOne(request):
    """
    the api of cancel Resource on one day (resource_one).
    POST takes resource_one_id as argument, and returns
    {'success': 1, 'resource_one_id'} or {'error': reason}.
    """
    if request.method == 'POST':
        if not _check_superuser(request.user):
            return _json_response({'error': 'Permission denied'})
        resource_one_id = request.POST['resource_one_id']
        if (resource_one_id is None) or (resource_one_id.strip() == ''):
            return _json_response({'error': 'Missing necessary fields'})
        res = models.cancelResourceOne(resource_one_id)
        if res['success']:
            return _json_response({'success': 1, 'resource_one_id':
                resource_one_id})
        else:
            return _json_response({'error': res['reason']})
    else:
        raise Http404

def listApplies(request):
    """
    list applies of a resource_one, or all unreplied applies, sort by ctime.
    GET takes resource_one_id as argument, if resource_one_id is present, then
    return all applies for that resource_one, or else return all unreplied
    applies.
    returns {'applies': [{
        'apply_id',
        'resource': {'resource_id', 'name', 'ctime'},
        'resource_one': {'resource_one_id', 'year', 'month', 'day'},
        'user': {'id', 'name', 'department', 'student_class', 'is_team_member',
            'team_category', 'team_role'},
        'contact_info',
        'reason',
        'state',
        'ctime'}, ...]}
    """
    if request.method == 'GET':
        if not _check_superuser(request.user):
            return _json_response({'error': 'Permission denied'})
        resource_one_id = request.GET.get('resource_one_id')
        if (resource_one_id is None) or (resource_one_id.strip() == ''):
            resource_one_id = ''
        res = models.listApplies(resource_one_id)
        return _json_response(res)
    else:
        raise Http404

def replyApply(request):
    """
    reply to an application, accept one will deny the others of the same
    resource_one.
    GET takes apply_id, accept(true|false), explanation(can be empty) as
    argument.
    returns {'success': 1, 'apply_id'} or {'error': reason}.
    """
    if request.method == 'GET':
        if not _check_superuser(request.user):
            return _json_response({'error': 'Permission denied'})
        if (not request.GET.has_key('apply_id')) or (not
                request.GET.has_key('accept')) :
            return _json_response({'error': 'Missing necessary fields'})
        apply_id = request.GET['apply_id']
        accept = request.GET['accept']
        if (apply_id is None) or (apply_id.strip() == '') or (
                accept is None) or (accept.strip() == ''):
            return _json_response({'error': 'Missing necessary fields'})
        if (not request.GET.has_key('explanation')):
            explanation = ''
        else:
            explanation = request.GET['explanation']
        if accept == 'true':
            res = models.acceptApply(apply_id, explanation)
        elif accept == 'false':
            res = models.denyApply(apply_id, explanation)
        else:
            return _json_response({'error': 'Incorrect accept format'})
        if res['success']:
            return _json_response({'success': 1, 'apply_id': apply_id})
        else:
            return _json_response({'error': res['reason']})
    else:
        raise Http404


def listResources(request):
    """
    list resources of one month that are available.
    GET takes year, month(default current year and month), showall (=true or
    false, default false) as argument
    returns json like
    {'resources' : [res_1, res_2, ... , res_30], 'days': 30, 'first_day': 2]}
    in which res_n is the resources in day n of this month, forms as
    [{'resource_id', 'resource_one_id', 'name', 'state'}, { ... }, ...]
    days is the total days of that month. first_day is that month's first
    day in the week, for example, first_day=1 presents the month's first day is
    Monday.
    """
    if request.method == 'GET':
        if not _check_active(request.user):
            return _json_response({'error': 'Permission denied'})
        year = request.GET.get('year')
        month = request.GET.get('month')
        showall = request.GET.get('showall')
        if (year is None) or (year.strip() == '') or (month is None) or (
                month.strip() == ''):
            current = time.localtime()
            year = current[0]
            month = current[1]
        else:
            year = int(year)
            month = int(month)
        if showall == "true":
            showall = True
        else:
            showall = False
        res = models.listResources(year, month, showall)
        return _json_response(res)
    else:
        raise Http404



def viewResource(request):
    """
    view a resource.
    GET takes resource_id as argument
    returns {'resource_id', 'name', 'description', 'ctime', 'resource_ones':
    [{'resource_one_id', 'year', 'month', 'day', 'state'}, ...]}
    """
    if request.method == 'GET':
        if not _check_active(request.user):
            return _json_response({'error': 'Permission denied'})
        resource_id = request.GET.get('resource_id')
        if (resource_id is None) or (resource_id.strip() == ''):
            return _json_response({'error': 'Missing necessary fields'})
        res = models.viewResource(resource_id)
        return _json_response(res)
    else:
        raise Http404

def applyResource(request):
    """
    the api of applying for a resource_one.
    POST takes resource_one_id, contact_info, and reason
    returns {'success': 1, 'apply_id'} or {'error': reason}.
    """
    if request.method == 'POST':
        user = request.user
        if not _check_active(user):
            return _json_response({'error': 'Permission denied'})
        resource_one_id = request.POST['resource_one_id']
        contact_info = request.POST['contact_info']
        reason = request.POST['reason']
        if (resource_one_id is None) or (contact_info is None) or (
                reason is None) or (resource_one_id.strip() == '') or (
                        contact_info.strip() == '') or (reason.strip() == ''):
            return _json_response({'error': 'Missing necessary fields'})
        res = models.addApply(resource_one_id, user.id, contact_info, reason)
        if res['success']:
            return _json_response({
                'success': 1,
                'apply_id': res['apply_id'].__str__()
                })
        else:
            return _json_response({'error': res['reason']})
    else:
        raise Http404

def listMyApplies(request):
    """
    list applies of the current user.
    GET
    returns {'applies': [{
        'resource': {'resource_id', 'name', 'ctime'},
        'resource_one': {'resource_one_id', 'year', 'month', 'day'},
        'contact_info',
        'reason',
        'state',
        'ctime'}, ...]}
    """
    if request.method == 'GET':
        user = request.user
        if not _check_active(user):
            return _json_response({'error': 'Permission denied'})
        res = models.listMyApplies(user.id)
        return _json_response(res)
    else:
        raise Http404

