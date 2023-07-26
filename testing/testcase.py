from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from rest_framework.test import APIClient

class TestCase(DjangoTestCase):
    def create_user(self, username, password='password', email='hello@mail.com'):
       return User.objects.create_user(username=username, password=password, email=email)
    
    def create_client(self):
        return APIClient()
    
    def create_tweet(self, user, content="default tweet."):
        return Tweet.objects.create(user=user, content=content)