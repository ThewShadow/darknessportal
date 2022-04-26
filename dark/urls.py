from django.contrib import admin
from django.urls import path, include
import main.urls as urls
import dark.settings as settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dark/', include('main.urls'), name='home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
