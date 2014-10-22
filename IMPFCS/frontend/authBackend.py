from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse
from urllib2 import urlopen, Request
from urllib import urlencode
import json


class THUAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        #####################################
        #change this after get the API
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                if user.check_password(password):
                    return user
                else:
                    return None
        except User.DoesNotExist:
            pass
        import THU_auth.views
        from django.http import HttpRequest
        request = HttpRequest()
        request.POST['username'] = username
        request.POST['password'] = password
        response = THU_auth.views.auth(request)
        #####################################
        ret = json.loads(response.content)
        if ret['valid'] == False:  #valid Tsinghua account
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.is_active = False  #will become active once his/her information is completed 
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
