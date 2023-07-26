from testing.testcase import TestCase
from tweets.models import Tweet
from django.contrib.auth.models import User
from datetime import timedelta
from utils.time_helpers import utc_now
# Create your tests here.
LIST_API = "/api/tweets/"
CREATE_API = "/api/tweets/"
class TweetTest(TestCase):
    def setUp(self):
        self.anonymous_client = self.create_client()
        self.user1_client = self.create_client()
        self.user1 = self.create_user(username="user1")
        self.user1_client.force_authenticate(self.user1)
        self.tweets1 = [self.create_tweet(self.user1) for _ in range(3)]

        self.user2 = self.create_user(username="user2")
        self.tweets2 = [self.create_tweet(self.user2) for _ in range(2)]

    def testHoursToNow(self):
        user = User.objects.create_user(username='hello')
        tweet = Tweet.objects.create(user=user, content="hello world")
        tweet.created_at = utc_now() - timedelta(hours=10)
        self.assertEqual(tweet.hours_to_now, 10)

    def test_list_api(self):
        response = self.anonymous_client.get(LIST_API)
        self.assertEqual(response.status_code, 400)

        response = self.anonymous_client.get(LIST_API, {"user_id": self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)

        response = self.anonymous_client.get(LIST_API, {"user_id": self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 2)

        response.data['tweets'][0]['id'] == self.tweets2[1].id
        response.data['tweets'][1]['id'] == self.tweets2[0].id

    def test_create_api(self):
        response = self.anonymous_client.post(CREATE_API)
        self.assertEqual(response.status_code, 403)

        response = self.user1_client.post(CREATE_API, {"content": "1"})
        self.assertEqual(response.status_code, 400)
        
        response = self.user1_client.post(CREATE_API, {"content": "1"*200})
        self.assertEqual(response.status_code, 400)

        tweet_count = Tweet.objects.count()
        response = self.user1_client.post(CREATE_API, {"content": "good night"})
        self.assertEqual(response.status_code, 201)
        print(response.data)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweet_count + 1)


