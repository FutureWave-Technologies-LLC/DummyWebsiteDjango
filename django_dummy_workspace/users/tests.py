from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import users
import hashlib

class UsersViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()

        # Sample user data for testing
        self.user_data = {
            "username": "testuser",
            "password": hashlib.sha256("password123".encode()).hexdigest(),
            "first_name": "Test",
            "last_name": "User",
            "profile_image": "",
        }
        self.user = users.objects.create(**self.user_data)

    # Test GET all users
    def test_get_users(self):
        response = self.client.get('user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    # Test GET user by ID (valid user)
    def test_get_user_data_valid(self):
        response = self.client.get(f'user/{self.user.user_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')    

    # Test user authentication with correct credentials
    def test_authenticate_user_success(self):
        data = {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post('authenticate_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token_id', response.data)
        self.assertEqual(response.data['username'], 'testuser')

    # Test user authentication with incorrect password
    def test_authenticate_user_failure(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        response = self.client.post('/authenticate_user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Password was not valid')

    # Test user login with correct credentials
    def test_login_user_success(self):
        response = self.client.get('login/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Successful login for testuser')

    # Test user login with invalid username
    def test_login_user_invalid_username(self):
        response = self.client.get('login/', {'username': 'wronguser', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Invalid Username')

    # Test user login with incorrect password
    def test_login_user_invalid_password(self):
        response = self.client.get('login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Invalid Password')

    # Test user signup with valid data
    def test_signup_user_valid(self):
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "profile_image": "",
        }
        response = self.client.post('sign_up/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['response'], 'User was created')

    # Test user signup with existing username
    def test_signup_user_existing_username(self):
        data = {
            "username": "testuser",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
            "profile_image": "",
        }
        response = self.client.post('sign_up/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Username already exists.')

    # Test user signup with invalid password
    def test_signup_user_invalid_password(self):
        data = {
            "username": "shortpassworduser",
            "password": "123",
            "first_name": "Short",
            "last_name": "Password",
            "profile_image": "",
        }
        response = self.client.post('sign_up/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Password must be more than 4 characters long.')

    # Test user search (match found)
    def test_search_users_found(self):
        response = self.client.get('search_users/', {'query': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'testuser')

    # Test user search (no match found)
    def test_search_users_not_found(self):
        response = self.client.get('search_users/', {'query': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Response'], 'No matching user found for: nonexistent')

    # Test update user settings (valid)
    def test_update_settings_valid(self):
        data = {
            "user_id": self.user.user_id,
            "profile_image": "new_image.jpg"
        }
        response = self.client.post('update_settings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_image, "new_image.jpg")

    # Test update user settings (user not found)
    def test_update_settings_user_not_found(self):
        data = {
            "user_id": 999,
            "profile_image": "new_image.jpg"
        }
        response = self.client.post('update_settings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
