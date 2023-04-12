from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from .models import Album, Photo
from .serializers import PublicAlbumSerializer, PrivateAlbumSerializer, PhotoSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class PublicAlbumList(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = PublicAlbumSerializer

    def get_queryset(self):
        return Album.objects.filter(is_private=False)


class PrivateAlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.all()
    serializer_class = PrivateAlbumSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Album.objects.filter(author=self.request.user)


class PublicAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = PublicAlbumSerializer


    def get_queryset(self):
        return Album.objects.filter(is_private=False)


class PrivateAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = PublicAlbumSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
