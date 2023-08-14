
from testing.testcase import TestCase
from friendship.models import Friendship

FOLLOW_URL = '/api/friendship/{}/follow/'
UNFOLLOW_URL = '/api/friendship/{}/unfollow/'
FOLLOWING_URL = '/api/friendship/{}/followings/'
FOLLOWER_URL = '/api/friendship/{}/followers/'

class FriendshipTest(TestCase):
    def setUp(self):
        self.user1 = self.create_user(username="username1")
        self.user1_client = self.create_client()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user(username="username2")
        self.user2_client = self.create_client()
        self.user2_client.force_authenticate(self.user2)

        self.anonymous_client = self.create_client()

    def testFollow(self):
        url = FOLLOW_URL.format(self.user1.id)
        # Not logged in
        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 403)
        # Method get 
        response = self.user2_client.get(url)
        self.assertEqual(response.status_code, 405)
        # Follow oneself
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, 400)
        # Success
        response = self.user2_client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], True)
        # repeated follow
        response = self.user2_client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['duplicate'], True)
        # follow back
        count = Friendship.objects.count()
        response = self.user1_client.post(FOLLOW_URL.format(self.user2.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count + 1, Friendship.objects.count())

    def testUnfollow(self):
        url = UNFOLLOW_URL.format(self.user1.id)
        # Not logged in
        response = self.anonymous_client.post(url)
        self.assertEqual(response.status_code, 403)
        # Method get 
        response = self.user2_client.get(url)
        self.assertEqual(response.status_code, 405)
        # Unfollow oneself
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, 400)
        # Success
        Friendship.objects.create(from_user=self.user2, to_user=self.user1)
        count = Friendship.objects.count()
        response = self.user2_client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], 1)
        self.assertEqual(Friendship.objects.count(), count - 1)
        # Unfollow unexisting friendship
        response = self.user2_client.post(url)
        count = Friendship.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['deleted'], 0)
        self.assertEqual(Friendship.objects.count(), count)

    def setupFollowing(self):
        u3 = self.create_user(username='username3')
        u4 = self.create_user(username='username4')
        Friendship.objects.create(from_user=self.user1, to_user=self.user2)
        Friendship.objects.create(from_user=self.user1, to_user=u3)
        Friendship.objects.create(from_user=self.user1, to_user=u4)
        

    def testFollowings(self):
        self.setupFollowing()
        url = FOLLOWING_URL.format(self.user1.id)
        # Method post 
        response = self.user2_client.post(url)
        self.assertEqual(response.status_code, 405)
        # Success
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, 200)
        followings = response.data['followings'] 
        self.assertEqual(len(followings), 3)
        t1 = followings[0]['created_at']
        t2 = followings[1]['created_at'] 
        t3 = followings[2]['created_at']
        self.assertEqual(t1>t2>t3, True)

    def setupFollower(self):
        u3 = self.create_user(username='username3')
        u4 = self.create_user(username='username4')
        Friendship.objects.create(from_user=self.user2, to_user=self.user1)
        Friendship.objects.create(from_user=u3, to_user=self.user1)
        Friendship.objects.create(from_user=u4, to_user=self.user1)    

    def testFollowers(self):
        self.setupFollower()
        url = FOLLOWER_URL.format(self.user1.id)
        # Method post 
        response = self.user1_client.post(url)
        self.assertEqual(response.status_code, 405)
        # Success
        response = self.user1_client.get(url)
        self.assertEqual(response.status_code, 200)
        followers = response.data['followers'] 
        self.assertEqual(len(followers), 3)
        t1 = followers[0]['created_at']
        t2 = followers[1]['created_at'] 
        t3 = followers[2]['created_at']
        self.assertEqual(t1>t2>t3, True)