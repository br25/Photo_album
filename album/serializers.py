from rest_framework import serializers
from .models import Album, Photo
from rest_framework.exceptions import PermissionDenied
from django.db import transaction


class PhotoSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())

    class Meta:
        model = Photo
        fields = ('id', 'title', 'image', 'created', 'author', 'album')
        read_only_fields = ('created', 'author')


    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.is_anonymous:
            raise PermissionDenied("Only authenticated users can create photos.")

        album = validated_data.pop('album')
        return Photo.objects.create(author=user, album=album, **validated_data)



class AlbumSerializer(serializers.ModelSerializer):
    photos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Photo.objects.all()
    )

    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'category', 'author', 'photos')
        extra_kwargs = {'photos': {'write_only': True}}


    @transaction.atomic
    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        album = Album.objects.create(**validated_data)
        album.photos.set(photos_data)
        return album







