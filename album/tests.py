from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Album, Photo
from .serializers import PublicAlbumSerializer, PrivateAlbumSerializer, PhotoSerializer
from auth_app.models import User



class AlbumViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@gmail.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.public_album = Album.objects.create(
            name='Public Album',
            description='Public album for all users',
            category=Album.Category.FAMILY,
            is_private=False,
            author=self.user,
        )
        self.private_album = Album.objects.create(
            name='Private Album',
            description='Private album for authenticated users',
            category=Album.Category.FAMILY,
            is_private=True,
            author=self.user,
        )
        self.client = APIClient()
        self.client.login(email='test@gmail.com', password='testpass')
        self.public_album_list_url = reverse('public-album-list')
        self.private_album_list_url = reverse('private-album-list')
        self.public_album_detail_url = reverse(
            'public-album-detail', kwargs={'pk': self.public_album.pk})
        self.private_album_detail_url = reverse(
            'private-album-detail', kwargs={'pk': self.private_album.pk})


    def test_public_album_list(self):
        response = self.client.get(self.public_album_list_url)
        albums = Album.objects.filter(is_private=False)
        serializer = PublicAlbumSerializer(albums, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_private_album_list(self):
        response = self.client.get(self.private_album_list_url)
        albums = Album.objects.filter(author=self.user)
        serializer = PrivateAlbumSerializer(albums, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_private_album(self):
        album_data = {
            'name': 'Test Album',
            'description': 'Test album for authenticated users',
            'category': Album.Category.FAMILY,
            'is_private': True,
            'author': self.user.pk, # Pass the user id instead of user object
        }
        response = self.client.post(
            self.private_album_list_url, album_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_public_album_detail(self):
        response = self.client.get(self.public_album_detail_url)
        album = Album.objects.get(pk=self.public_album.pk)
        serializer = PublicAlbumSerializer(album)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_private_album_detail(self):
        response = self.client.get(self.private_album_detail_url)
        album = Album.objects.get(pk=self.private_album.pk)
        serializer = PrivateAlbumSerializer(album)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_private_album_detail(self):
        album_data = {
            'name': 'Updated Album',
            'description': 'Updated album for authenticated users',
            'category': Album.Category.FAMILY,
            'is_private': True,
            'author': self.user.pk, # Pass the user id instead of user object
        }
        response = self.client.put(
            self.private_album_detail_url, album_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_private_album_detail(self):
        response = self.client.delete(self.private_album_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

