from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from .models import Album, Photo
from .serializers import AlbumSerializer, AlbumSerializer, PhotoSerializer
from .permission import IsOwner



class PublicAlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.filter(is_published=True)
    serializer_class = AlbumSerializer

    def perform_create(self, serializer):
        serializer.save()


class PrivateAlbumList(generics.ListCreateAPIView):
    queryset = Album.objects.filter(is_published=False)
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
