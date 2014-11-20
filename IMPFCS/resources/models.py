from bson import ObjectId
from django.contrib.auth.models import User
import pymongo
import calendar
import time
import mongo
mclient = mongo.MongoClient()

def addResource(name, description, dates):
    resource_id = mclient.insert_doc('resource', {
        'name': name,
        'description': description,
        'ctime': time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        })
    dateList = dates.split(';')
    resource_ones = []
    for date in dateList:
        d = date.split('-')
        resource_ones.append({
            'resource_id': resource_id,
            'year': int(d[0]),
            'month': int(d[1]),
            'day': int(d[2]),
            'state': 'available'
        })
    mclient.db.resource_one.insert(resource_ones)
    return resource_id

def cancelResource(resource_id):
    mclient.db['resource_one'].update({'resource_id': ObjectId(resource_id)},
            {'$set': {'state': 'cancelled'}}, multi=True)
    mclient.db['apply'].update({'resource_id': ObjectId(resource_id),
        'state': {'$in': ['unreplied', 'accepted']}}, {
        '$set': {'state': 'denied', 'reply': 'Resource has been cancelled'}},
        multi=True)
    return {'success': True}

def cancelResourceOne(resource_one_id):
    mclient.db['resource_one'].update({'_id': ObjectId(resource_one_id)}, {
        '$set': {'state': 'cancelled'}})
    mclient.db['apply'].update({'resource_one_id': ObjectId(resource_one_id),
        'state': {'$in': ['unreplied', 'accepted']}}, {
        '$set': {'state': 'denied', 'reply': 'Resource has been cancelled'}},
        multi=True)
    return {'success': True}

def listApplies(resource_one_id):
    if resource_one_id == '':
        applies = mclient.db['apply'].find({'state': 'unreplied'})
    else:
        applies = mclient.db['apply'].find(
                {'resource_one_id': ObjectId(resource_one_id)})
    applies = applies.sort('ctime', pymongo.ASCENDING)
    table = {}
    res = []
    for a in applies:
        if not table.has_key(a['resource_id']):
            table[a['resource_id']] = mclient.db['resource'].find_one(
                    {'_id': a['resource_id']})
        resource = table[a['resource_id']]
        if not table.has_key(a['resource_one_id']):
            table[a['resource_one_id']] = mclient.db['resource_one'].find_one(
                    {'_id': a['resource_one_id']})
        resource_one = table[a['resource_one_id']]
        user = User.objects.get(id=a['user_id'])
        res.append({
            'apply_id': a['_id'].__str__(),
            'resource': {
                'resource_id': resource['_id'].__str__(),
                'name': resource['name'],
                'ctime': resource['ctime']},
            'resource_one': {
                'resource_one_id': resource_one['_id'].__str__(),
                'year': resource_one['year'],
                'month': resource_one['month'],
                'day': resource_one['day']},
            'user': {
                'id': user.id,
                'name': user.userinfo.name,
                'department': user.userinfo.department,
                'student_class': user.userinfo.studentClass,
                'is_team_member': user.userinfo.is_teamMember,
                'team_category': user.userinfo.teamCategory,
                'team_role': user.userinfo.teamRole},
            'contact_info': a['contact_info'],
            'reason': a['reason'],
            'state': a['state'],
            'reply': a['reply'],
            'ctime': a['ctime']})
    return {'applies': res}


def acceptApply(apply_id, explanation):
    a = mclient.db['apply'].find_one({'_id': ObjectId(apply_id)})
    resource_one_id = a['resource_one_id']
    mclient.db['resource_one'].update({'_id': resource_one_id},
            {'$set': {'state': 'distributed'}})
    mclient.db['apply'].update({'resource_one_id': resource_one_id,
        'state': {'$in': ['unreplied', 'accepted']}},
            {'$set': {'state': 'denied',
            'reply': 'Resource has been distributed'}}, multi=True)
    mclient.db['apply'].update({'_id': ObjectId(apply_id)},
            {'$set': {'state': 'accepted', 'reply': explanation}})
    return {'success': True}


def denyApply(apply_id, explanation):
    mclient.db['apply'].update({'_id': ObjectId(apply_id)},
            {'$set': {'state': 'denied', 'reply': explanation}})
    return {'success': True}


def listResources(year, month, showall):
    if showall:
        resource_ones = mclient.db['resource_one'].find(
                {'year': year, 'month': month})
    else:
        resource_ones = mclient.db['resource_one'].find(
                {'year': year, 'month': month, 'state': 'available'})
    monthrange = calendar.monthrange(year, month)
    first_day = monthrange[0] + 1
    days = monthrange[1]
    resources = [[] for i in range(days)]
    # saving resource docs, id as key, doc as value
    # cache this may give a better performance
    rs = {}
    for resource_one in resource_ones:
        if not rs.has_key(resource_one['resource_id']):
            rs[resource_one['resource_id']] = mclient.db['resource'].find_one(
                    {'_id': resource_one['resource_id']})
        resource = rs[resource_one['resource_id']]

        resources[resource_one['day'] - 1].append({
            'resource_id': resource_one['resource_id'].__str__(),
            'resource_one_id': resource_one['_id'].__str__(),
            'name': resource['name'],
            'state': resource_one['state']
            })
    return {'resources': resources, 'days': days, 'first_day': first_day,
            'year': year, 'month': month}


def viewResource(resource_id):
    resource = mclient.db['resource'].find_one({'_id': ObjectId(resource_id)})
    resource_ones = mclient.db['resource_one'].find(
            {'resource_id': ObjectId(resource_id)})
    return {
            'resource_id': resource_id,
            'name': resource['name'],
            'description': resource['description'],
            'resource_ones': [{
                'resource_one_id': ro['_id'].__str__(),
                'year': ro['year'],
                'month': ro['month'],
                'day': ro['day'],
                'state': ro['state']
                } for ro in resource_ones]
            }

def addApply(resource_one_id, user_id, contact_info, reason):
    resource_one = mclient.db['resource_one'].find_one(
            {'_id': ObjectId(resource_one_id)})
    if resource_one is None:
        return {'success': False,
                'reason': 'The resource you apply for does not exist'}
    count = mclient.db['apply'].find({'user_id': user_id,
        'resource_one_id': ObjectId(resource_one_id)}).count()
    if count != 0:
        return {'success': False,
                'reason': 'You have already applied'}
    if resource_one['state'] == 'available':
        apply_id = mclient.insert_doc(
                'apply', {
                    'resource_id': resource_one['resource_id'],
                    'resource_one_id': ObjectId(resource_one_id),
                    'user_id': user_id,
                    'contact_info': contact_info,
                    'reason': reason,
                    'ctime': time.strftime(
                        '%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    'state': 'unreplied',
                    'reply': ''})
        return {'success': True, 'apply_id': apply_id.__str__()}
    elif resource_one['state'] == 'cancelled':
        return {'success': False,
                'reason': 'The resource you apply for has been cancelled'}
    elif resource_one['state'] == 'distributed':
        return {'success': False,
                'reason': 'The resource you apply for has been distributed'}
    return {'success': False,
            'reason': 'The resource you apply for is not available'}


def listMyApplies(user_id):
    applies = mclient.db['apply'].find({'user_id': user_id})
    applies = applies.sort('ctime', pymongo.ASCENDING)
    table = {}
    res = []
    for a in applies:
        if not table.has_key(a['resource_id']):
            table[a['resource_id']] = mclient.db['resource'].find_one(
                    {'_id': a['resource_id']})
        resource = table[a['resource_id']]
        if not table.has_key(a['resource_one_id']):
            table[a['resource_one_id']] = mclient.db['resource_one'].find_one(
                    {'_id': a['resource_one_id']})
        resource_one = table[a['resource_one_id']]
        res.append({
            'apply_id': a['_id'].__str__(),
            'resource': {
                'resource_id': resource['_id'].__str__(),
                'name': resource['name'],
                'ctime': resource['ctime']},
            'resource_one': {
                'resource_one_id': resource_one['_id'].__str__(),
                'year': resource_one['year'],
                'month': resource_one['month'],
                'day': resource_one['day']},
            'contact_info': a['contact_info'],
            'reason': a['reason'],
            'state': a['state'],
            'reply': a['reply'],
            'ctime': a['ctime']})
    return {'applies': res}
