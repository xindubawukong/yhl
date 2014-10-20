from django.test import TestCase
from django.core.urlresolvers import reverse


class TestAddUser(TestCase):

    def test_add_user_without_username(self):
        response = self.client.post(reverse('users:addUser'), {'password': 'ABC1234567'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_without_password(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'ABC1234567'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_with_empty_username(self):
        response = self.client.post(reverse('users:addUser'), {'username': '', 'password': 'ABC1234567'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_with_empty_password(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': ''})
        self.assertEqual(response.status_code, 404)

    def test_add_users_with_same_username(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABC1234567'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': 'ABasdf567'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_with_naive_password(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': '123'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_with_illegal_username(self):
        response = self.client.post(reverse('users:addUser'), {'username': '%$^@#$', 'password': 'ABC1234567'})
        self.assertEqual(response.status_code, 404)

    def test_add_user_with_illegal_password(self):
        response = self.client.post(reverse('users:addUser'), {'username': 'woshishabi', 'password': '  '})
        self.assertEqual(response.status_code, 404)
