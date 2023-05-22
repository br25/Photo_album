from rest_framework import serializers
from .models import Album, Photo
from drf_extra_fields.fields import Base64ImageField
from django.db import transaction


class PhotoSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())

    class Meta:
        model = Photo
        fields = ('id', 'title', 'image', 'created', 'author', 'album')
        read_only_fields = ('created', 'author')

    def create(self, validated_data):
        user = self.context['request'].user
        author = validated_data.pop('author', None)
        album = validated_data.pop('album')
        return Photo.objects.create(author=author or user, album=album, **validated_data)



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







