from django.test import TestCase, Client  
from django.urls import reverse  
from rest_framework import status  
from rest_framework.test import APIClient  
from .models import users, follow  

# Create your tests here.

#class HomeViewTestCase(TestCase):
#    def setUp(self):
#        self.client = Client()

#    def test_home_status_code(self):
#        response = self.client.get(reverse('home'))
#        self.assertEqual(response.status_code, 200)

#    def test_home_template_used(self):
#        response = self.client.get(reverse('home'))
#        self.assertTemplateUsed(response, 'home.html')

#class GetUsersTestCase(TestCase):
#    def setUp(self):
#        self.user1 = users.objects.create(username="testuser1", user_id=1)
#        self.user2 = users.objects.create(username="testuser2", user_id=2)

#    def test_get_users_status_code(self):
#        response = self.client.get(reverse('get_users'))
#        self.assertEqual(response.status_code, 200)

#    def test_get_users_response_data(self):
#        response = self.client.get(reverse('get_users'))
#        self.assertEqual(len(response.data), 2)
#        self.assertEqual(response.data[0]['username'], "testuser1")

#class GetUserDataTestCase(TestCase):
#    def setUp(self):
#        self.user = users.objects.create(username="testuser", user_id=1)

#    def test_get_user_data_valid(self):
#        response = self.client.get(reverse('get_user_data'), {'user_id': 1})
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.json()["username"], "testuser")
#        self.assertFalse(response.json()["error"])

#    def test_get_user_data_invalid(self):
#        response = self.client.get(reverse('get_user_data'), {'user_id': 999})
#        self.assertEqual(response.status_code, 200)
#        self.assertTrue(response.json()["error"])
#        self.assertEqual(response.json()["response"], "User with this ID cannot be found")

#class AuthenticateUserTestCase(TestCase):
#    def setUp(self):
#        self.user = users.objects.create(username="testuser", password="securepassword", user_id=1)

#    def test_authenticate_user_valid(self):
#        response = self.client.post(reverse('authenticate_user'), {'username': 'testuser', 'password': 'securepassword'})
#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.json()["user_id"], 1)
#        self.assertIn("token_id", response.json())

#    def test_authenticate_user_invalid_password(self):
#        response = self.client.post(reverse('authenticate_user'), {'username': 'testuser', 'password': 'wrongpassword'})
#        self.assertEqual(response.status_code, 200)
#        self.assertTrue(response.json()["error"])
#        self.assertEqual(response.json()["response"], "Password was not valid")

class SignupUserTestCase(TestCase):
    def test_signup_user_valid(self):
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser', 'password': 'validpass',
            'first_name': 'John', 'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["error"])
        print("User saved:", User.objects.filter(username="newuser").exists())

    def test_signup_user_username_taken(self):
        users.objects.create(username="newuser")
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser', 'password': 'validpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["error"])
        self.assertEqual(response.json()["response"], "Username already exists, please choose another username")

    def test_signup_user_short_password(self):
        response = self.client.post(reverse('sign_up'), {
            'username': 'newuser', 'password': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["error"])
        self.assertEqual(response.json()["response"], "Password must be more than 4 characters long")

#class LoginUserTestCase(TestCase):
#    def setUp(self):
#        self.user = users.objects.create(username="testuser", password="securepassword")

#    def test_login_user_valid(self):
#        response = self.client.get(reverse('login'), {'username': 'testuser', 'password': 'securepassword'})
#        self.assertEqual(response.status_code, 200)
#        self.assertFalse(response.json()["error"])

#    def test_login_user_invalid_username(self):
#        response = self.client.get(reverse('login'), {'username': 'wronguser', 'password': 'securepassword'})
#        self.assertEqual(response.status_code, 200)
#        self.assertTrue(response.json()["error"])
#        self.assertEqual(response.json()["response"], "Username is not valid")

#    def test_login_user_invalid_password(self):
#        response = self.client.get(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
#        self.assertEqual(response.status_code, 200)
#        self.assertTrue(response.json()["error"])
#        self.assertEqual(response.json()["response"], "Password is not valid")