from rest_framework import serializers
from .models import Album, Photo


class PublicAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'category', 'is_private')


class PrivateAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('id', 'name', 'description', 'category', 'is_private')



class PhotoSerializer(serializers.ModelSerializer):
    album = serializers.PrimaryKeyRelatedField(queryset=Album.objects.all())

    class Meta:
        model = Photo
        fields = ('id', 'title', 'image', 'created', 'author', 'album')
        read_only_fields = ('created', )

    def create(self, validated_data):
        user = self.context['request'].user
        author = validated_data.pop('author', None)
        album = validated_data.pop('album')
        return Photo.objects.create(author=author or user, album=album, **validated_data)