# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from .models import User


# class UserViewTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='test_password',
#             first_name='John',
#             last_name='Doe',
#         )
#         self.client.force_authenticate(user=self.user)

#     def test_list_users(self):
#         response = self.client.get(reverse('users'))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

# class RegistrationViewTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.valid_payload = {
#             'first_name': 'John',
#             'last_name': 'Doe',
#             'email': 'test@example.com',
#             'password': 'test_password'
#         }

#     def test_create_user(self):
#         response = self.client.post(reverse('register'), data=self.valid_payload)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(User.objects.count(), 1)
#         self.assertEqual(User.objects.get().email, 'test@example.com')

#     def test_create_user_with_existing_email(self):
#         User.objects.create_user(
#             email='test@example.com',
#             password='test_password',
#             first_name='John',
#             last_name='Doe',
#         )
#         response = self.client.post(reverse('register'), data=self.valid_payload)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(User.objects.count(), 1)


# class LoginViewTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='test_password',
#             first_name='John',
#             last_name='Doe',
#         )

#     def test_login_with_valid_credentials(self):
#         response = self.client.post(reverse('login'), data={'email': 'test@example.com', 'password': 'test_password'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.data['detail'], 'Login successful.')

#     def test_login_with_invalid_credentials(self):
#         response = self.client.post(reverse('login'), data={'email': 'test@example.com', 'password': 'wrong_password'})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertIn('detail', response.data)
#         self.assertEqual(response.data['detail'], 'Invalid credentials.')


# class LogoutViewTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='test_password',
#             first_name='John',
#             last_name='Doe',
#         )
#         self.client.force_authenticate(user=self.user)
