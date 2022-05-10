from django.contrib import admin
from .models import Image
from .models import Video
from .models import User
from .models import Message


admin.site.register(Image)
admin.site.register(Video)
admin.site.register(User)
admin.site.register(Message)

