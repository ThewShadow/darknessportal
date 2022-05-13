from django.urls import path
from main.views import login
from main.views import register
from main.views import ImageDetailView
from main.views import logout
from main.views import IndexView
from main.views import AlbumView
from main.views import AddImageView
from main.views import get_messages
from main.views import UserDetail
from main.views import UserEditDetail


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('album/add/', AddImageView.as_view(), name='add_photo'),
    path('album/list/<int:page>', AlbumView.as_view(), name='album/list'),
    path('album/photo/<int:id>', ImageDetailView.as_view(), name='albumphoto'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('messages/get', get_messages),
    path('user/<int:id>', UserDetail.as_view(), name='user_profile'),
    path('user/update/<int:pk>/', UserEditDetail.as_view(), name='update_profile')
]
