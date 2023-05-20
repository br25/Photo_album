from django.urls import path
from .views import PublicAlbumList, PrivateAlbumList

urlpatterns = [
    path('albums/', PublicAlbumList.as_view(), name='public-album-list'),
    path('private/albums/', PrivateAlbumList.as_view(), name='private-album-list'),
    # path('albums/<int:pk>/', PublicAlbumDetail.as_view(), name='public-album-detail'),
    # path('private/albums/<int:pk>/', PrivateAlbumDetail.as_view(), name='private-album-detail'),
    # path('photos/', PhotoList.as_view(), name='photo-list'),
    # path('photos/<int:pk>/', PhotoDetail.as_view(), name='photo-detail'),
]
