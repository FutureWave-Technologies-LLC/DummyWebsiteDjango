from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import posts, users, comments, replies

class PostViewTests(APITestCase):
    
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Test Post", description="Test Desc", media="media")

    def test_get_post_not_found(self):
        url = reverse('post')  
        response = self.client.get(url, {'post_id': 99999})  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_post_success(self):
        url = reverse('post')  
        response = self.client.get(url, {'post_id': self.post.post_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['post_id'], self.post.post_id)

    def test_create_post_success(self):
        url = reverse('post')  
        data = {
            'user_id': self.user.user_id,
            'title': 'Test Post',
            'description': 'Test Description',
            'media': 'media_url'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['Response'], "Post was created")


class GetPostsViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        posts.objects.create(author=self.user, title="Post 1", description="Description 1", media="media1")
        posts.objects.create(author=self.user, title="Post 2", description="Description 2", media="media2")

    def test_get_all_posts(self):
        url = reverse('all_posts')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class GetRepliesViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Test Post", description="Test Desc", media="media")
        replies.objects.create(author=self.user, comment_id=1, reply="Test reply")

    def test_get_replies(self):
        url = reverse('replies')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


class CommentsViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(post_id=1, author=self.user, title="Test Post", description="Test Desc", media="media")
        comments.objects.create(author=self.user, post=self.post, comment="This is a test comment")

    def test_get_comments_success(self):
        url = reverse('comments')  
        response = self.client.get(url, {'post_id': self.post.post_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)

    def test_create_comment_success(self):
        url = reverse('comments')
        data = {
            "user_id": self.user.user_id,
            "post_id": self.post.post_id,
            "comment": "A new test comment"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('Response'), "Commented created")

class CreatePostViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.url = reverse('post')  

    def test_create_post(self):
        data = {
            'user_id': self.user.user_id,
            'title': 'New Post Title',
            'description': 'New post description',
            'media': 'media_url'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['Response'], "Post was created")

class GetPostViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Test Post", description="Test Desc", media="media")
        self.url = reverse('post')  

    def test_get_post(self):
        response = self.client.get(f'{self.url}?post_id={self.post.post_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['post_id'], self.post.post_id)
        self.assertEqual(response.json()['title'], self.post.title)

class GetAllPostsViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.posts = [
            posts.objects.create(author=self.user, title=f"Post {i}", description=f"Description {i}", media="media_url") 
            for i in range(3)
        ]
        self.url = reverse('all_posts')  

    def test_get_all_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

class CreateCommentViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Test Post", description="Test Desc", media="media")
        self.url = reverse('comments')  

    def test_create_comment(self):
        data = {
            'user_id': self.user.user_id,
            'post_id': self.post.post_id,
            'comment': 'This is a test comment'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['Response'], "Commented created")

class GetCommentsViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Test Post", description="Test Desc", media="media")
        self.comment = comments.objects.create(author=self.user, post=self.post, comment="Test comment")
        self.url = reverse('comments')  

    def test_get_comments(self):
        response = self.client.get(f'{self.url}?post_id={self.post.post_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]['comment'], self.comment.comment)

class GetPostInvalidIDViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.url = reverse('post')  

    def test_get_post_invalid_id(self):
        response = self.client.get(f'{self.url}?post_id=9999')  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['response'], "Post with this ID cannot be found")

class UpdatePostViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Original Title", description="Original Description", media="media")
        self.url = reverse('post')

    def test_update_post_success(self):
        data = {
            'post_id': self.post.post_id,
            'title': 'Updated Title',
            'description': 'Updated Description',
            'media': 'updated_media'
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
        self.assertEqual(self.post.description, 'Updated Description')


class DeletePostViewTests(APITestCase):
    def setUp(self):
        self.user = users.objects.create(user_id=1, username="testuser")
        self.post = posts.objects.create(author=self.user, title="Title to be Deleted", description="Description", media="media")
        self.url = reverse('post')

    def test_delete_post_success(self):
        response = self.client.delete(f'{self.url}?post_id={self.post.post_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        response = self.client.get(f'{self.url}?post_id={self.post.post_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
