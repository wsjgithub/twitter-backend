from django.test import TestCase
from tweets.models import Tweet
from django.contrib.auth.models import User
from datetime import timedelta
from utils.time_helpers import utc_now
# Create your tests here.
class TweetTest(TestCase):
    def setUp(self):
        pass

    def testHoursToNow(self):
        user = User.objects.create_user(username='hello')
        tweet = Tweet.objects.create(user=user, content="hello world")
        tweet.created_at = utc_now() - timedelta(hours=10)
        self.assertEqual(tweet.hours_to_now, 10)