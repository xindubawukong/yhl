from django.test import TestCase
from django.core.urlresolvers import reverse
import json
import re


def errorResponse(response):
    if (response.status_code != 200):
        return False
    m = re.search(r'{(.*:.*)*}', str(response))
    if (m is None):
        return False
    ret = json.loads(m.group(0)) 
    if ret['error']:
        return True
    else:
        return False


def validResponse(response):
    if (response.status_code != 200):
        return False
    m = re.search(r'{(.*:.*)*}', str(response))
    if (m is None):
        return False
    ret = json.loads(m.group(0)) 
    if ret['error']:
        return False
    else:
        return True


class TestAddUser(TestCase):

    def test_add_user(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABC1234567'})
        self.assertTrue(validResponse(response))

    def test_add_user_without_username(self):
        response = self.client.post(reverse('users:addUser'), {'password': 'ABC1234567'})
        self.assertTrue(errorResponse(response))

    def test_add_user_without_password(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'ABC1234567'})
        self.assertTrue(errorResponse(response))

    def test_add_user_with_empty_username(self):
        response = self.client.post(reverse('users:addUser'), {'username': '', 'password': 'ABC1234567'})
        self.assertTrue(errorResponse(response))

    def test_add_users_with_same_username(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABC1234567'})
        self.assertTrue(validResponse(response))
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABasdf567'})
        self.assertTrue(errorResponse(response))


class TestUserLogin(TestCase):

    def test_user_login(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABC1234567'})
        self.assertTrue(validResponse(response))
        response = self.client.post(reverse('users:userLogin'), {'username': 'woshishabi', 'password': 'ABC1234567'})
        self.assertTrue(validResponse(response))

    def test_nonexist_user_login(self):
        response = self.client.post(reverse('users:userLogin'), {'username': 'haha', 'password': 'ABC1234567'})
        self.assertTrue(errorResponse(response))

    def test_user_login_without_username(self):
        response = self.client.post(reverse('users:userLogin'), {'password': 'ABC1234567'})
        self.assertTrue(errorResponse(response))

    def test_user_login_without_password(self):
        response = self.client.post(reverse('users:userLogin'), {'username': 'haha'})
        self.assertTrue(errorResponse(response))

    def test_user_login_with_empty_username(self):
        response = self.client.post(reverse('users:userLogin'), {'username': '', 'password': 'ABC1234567'})
        self.assertTrue(errorResponse(response))
