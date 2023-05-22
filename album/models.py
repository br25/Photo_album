from django.db import models
from auth_app.models import User
from django.utils.translation import gettext_lazy as _


class Album(models.Model):
    class Category(models.TextChoices):
        PRIVATE = 'PR', _('Private')
        PUBLIC = 'PB', _('Public')

    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.PUBLIC,
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums')

    photos = models.ManyToManyField('Photo', related_name='albums')

    def __str__(self):
        return self.name


def photo_format(instance, filename):
    return 'images/{0}/{1}'.format(instance.album, filename)


class Photo(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(_("Image"), upload_to=photo_format)
    created = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='albums')
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='author')

    def __str__(self):
        return self.title


