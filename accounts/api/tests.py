# from django.test import TestCase
from testing.testcase import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

LOGIN_URL = "/api/accounts/login/"
class AccountApiTest(TestCase):
    def setUp(self):
        # username, password, email = "testuser", "password", "abs@abc.com"
        # self.user = User.objects.create_user(username, email, password)
        self.user = self.create_user("testuser", "password", "abs@abc.com")
        self.client = APIClient()

    def test_login(self):
        # test with wrong method
        response = self.client.get(LOGIN_URL, {
            "username": self.user.username,
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 405)
        
        # test with wrong passwords
        response = self.client.post(LOGIN_URL, {
            "username": self.user.username,
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 400)
        STATUS_URL = "/api/accounts/login_status/"

        # test login status without logging in
        response = self.client.get(STATUS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["has_logged_in"], False)

        # test login with correct password
        response = self.client.post(LOGIN_URL,{
            "username": self.user.username,
            "password": "password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], "abs@abc.com")
        
        # test login status after logged in
        response = self.client.get(STATUS_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['has_logged_in'], True)

        
        