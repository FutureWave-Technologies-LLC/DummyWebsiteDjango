from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import follow
from users.models import users
from posts.models import posts

class ProfileViewsTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user_1 = users.objects.create(username='user1', password='password1')
        self.user_2 = users.objects.create(username='user2', password='password2')
        self.user_3 = users.objects.create(username='user3', password='password3')
        self.user_4 = users.objects.create(username='user4', password='password4')

        # Create test posts for user_1
        self.post_1 = posts.objects.create(
            author=self.user_1,
            title='Post 1',
            description='Description of Post 1',
            media=None,
        )
        self.post_2 = posts.objects.create(
            author=self.user_1,
            title='Post 2',
            description='Description of Post 2',
            media=None,
        )

        # Create follow relationships
        follow.objects.create(follower=self.user_1, followee_id=self.user_2.user_id)
        follow.objects.create(follower=self.user_2, followee_id=self.user_4.user_id)
        follow.objects.create(follower=self.user_2, followee_id=self.user_1.user_id)
        follow.objects.create(follower=self.user_4, followee_id=self.user_1.user_id)

        self.client = APIClient()

    def test_profile_posts(self):
        # Test profile_posts endpoint for returning posts of a user.
        url = reverse('profile_posts')
        response = self.client.get(url, {'user_id': self.user_1.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # user_1 has 2 posts
        self.assertIn('post_id', response.data[0])
        self.assertIn('title', response.data[0])
        self.assertIn('description', response.data[0])

    def test_profile_posts_empty(self):
        # Test profile_posts when no posts exist for the user.
        url = reverse('profile_posts')
        response = self.client.get(url, {'user_id': self.user_3.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # user_3 has no posts

    def test_following_get(self):
        # Test that following GET returns the users a user is following.
        url = reverse('following')
        response = self.client.get(url, {'user_id': self.user_1.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # user_1 follows user_2
        self.assertEqual(response.data[0]['username'], 'user2')

    def test_following_get_empty(self):
        # Test following GET when the user follows no one.
        url = reverse('following')
        response = self.client.get(url, {'user_id': self.user_3.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # user_3 follows no one

    def test_following_post_follow(self):
        # Test following POST when a user follows another user.
        url = reverse('following')
        data = {'followee_username': 'user2', 'follower_id': self.user_3.user_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Followed' in response.data)
        self.assertEqual(response.data['Followed'], True)

        # Ensure the follow relationship was created
        self.assertTrue(follow.objects.filter(follower_id=self.user_3.user_id, followee_id=self.user_2.user_id).exists())

    def test_following_post_unfollow(self):
        # Test following POST when a user unfollows another user.
        url = reverse('following')
        data = {'followee_username': 'user2', 'follower_id': self.user_1.user_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Followed' in response.data)
        self.assertEqual(response.data['Followed'], False)

        # Ensure the follow relationship was deleted
        self.assertFalse(follow.objects.filter(follower_id=self.user_1.user_id, followee_id=self.user_2.user_id).exists())

    def test_get_followers(self):
        # Test get_followers endpoint for returning list of followers.
        url = reverse('get_followers')
        response = self.client.get(url, {'user_id': self.user_2.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # user_2 has 1 follower, user_1
        self.assertEqual(response.data[0]['username'], 'user1')

    def test_get_followers_empty(self):
        # Test get_followers when a user has no followers.
        url = reverse('get_followers')
        response = self.client.get(url, {'user_id': self.user_3.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # user_3 has no followers

    def test_profile_posts_invalid_user(self):
        # Test profile_posts endpoint with an invalid user_id
        url = reverse('profile_posts')
        response = self.client.get(url, {'user_id': 999999})  # Invalid user_id
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Assuming the API returns an error message on failure

    def test_following_self(self):
        # Test that a user cannot follow themselves
        url = reverse('following')
        data = {'followee_username': 'user1', 'follower_id': self.user_1.user_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Assuming the API returns an error message

    def test_following_non_existing_user(self):
        # Test that a user cannot follow a non-existing user
        url = reverse('following')
        data = {'followee_username': 'nonexistentuser', 'follower_id': self.user_1.user_id}
        response = self.client.post(url, data, format='json')
        
        # Check that the response is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check that the response Content-Type is 'application/json'
        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
        
        # Check that the error message is returned
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Followee does not exist')

    def test_get_followers_multiple(self):
        # Test get_followers when the user has multiple followers
        url = reverse('get_followers')
        response = self.client.get(url, {'user_id': self.user_1.user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # user_1 has 2 followers: user_2 and user_3
        self.assertEqual(response.data[0]['username'], 'user2')
        self.assertEqual(response.data[1]['username'], 'user3')

    def test_unfollow_non_followed_user(self):
        # Test unfollowing a user who is not followed
        url = reverse('following')
        data = {'followee_username': 'user2', 'follower_id': self.user_1.user_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Assuming the API returns an error message

    def test_following_with_invalid_follower_id(self):
        # Test that following fails when the follower does not exist in the database
        url = reverse('following')
        data = {'followee_username': 'user2', 'follower_id': 9999}  # 9999 is an invalid ID
        response = self.client.post(url, data, format='json')
    
        # Check that the response status is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(response['Content-Type'], 'application/json; charset=utf-8')
    
        # Check that the response contains an error message
        self.assertIn('error', response.json())  # The response should be JSON
        self.assertEqual(response.json()['error'], 'Follower does not exist')
    
    def test_successful_unfollow(self):
        # Ensure the follow relationship exists first
        follow.objects.create(follower=self.user_1, followee_id=self.user_2.user_id)

        url = reverse('following')
    
        # Unfollow user_2
        data = {'followee_username': 'user2', 'follower_id': self.user_1.user_id}
        response = self.client.post(url, data, format='json')
    
        # Check that the response is OK and the user has unfollowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Followed', response.json())
        self.assertEqual(response.json()['Followed'], False)
    
        # Ensure the follow relationship was deleted
        self.assertFalse(follow.objects.filter(follower_id=self.user_1.user_id, followee_id=self.user_2.user_id).exists())
