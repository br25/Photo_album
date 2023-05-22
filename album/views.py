from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from .models import Album, Photo
from .serializers import AlbumSerializer, AlbumSerializer, PhotoSerializer
from .permission import IsOwner

from auth_app.models import User


class PublicAlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.filter(category="PB")
    serializer_class = AlbumSerializer

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        serialized_data = response.data

        # Modify serialized_data to include author username
        for data in serialized_data:
            author_id = data['author']
            user = User.objects.get(id=author_id)
            data['author'] = user.email

        response.data = serialized_data
        return response

class PrivateAlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.filter(category="PR")
    serializer_class = AlbumSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     return Album.objects.filter(author=self.request.user)


# class PublicAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Album.objects.all()
#     serializer_class = AlbumSerializer


#     def get_queryset(self):
#         return Album.objects.filter(is_private=False)


# class PrivateAlbumDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Album.objects.all()
#     serializer_class = AlbumSerializer
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated, IsOwner]


class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
