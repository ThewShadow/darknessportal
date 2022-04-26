from django.urls import path
from main.views import index
from main.views import album
from main.views import add_photo
from main.views import photo_detail

urlpatterns = [
    path('', index, name='home'),
    path('album/', album, name='album'),
    path('album/add/', add_photo, name='add_photo'),
    path('album/<int:id>', photo_detail, name='photo_detail')
]
