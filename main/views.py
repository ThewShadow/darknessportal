from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Image
import datetime
from .models import Video


def index(request):
    setquery = Image.objects.order_by('-pub_date')[:6]
    allnewvideos = Video.objects.order_by('-pub_date')[:5]
    context = {'new_photos': setquery, 'new_videos': allnewvideos}
    return render(request, 'main/index.html', context=context)


def album(request):
    allimages = Image.objects.order_by('-pub_date')
    context = {'all': allimages}
    return render(request, 'main/album.html', context=context)


def add_photo(request):
    if request.method == 'GET':
        return render(request, 'main/add_photo.html', )
    else:
        newimage = Image()
        newimage.author = 'vlad'
        newimage.pub_date = datetime.datetime.now()
        newimage.image = request.FILES['Image']
        newimage.save()
        return render(request, 'main/album.html', )

def photo_detail(request, id):
    obj = Image.objects.get(pk=id)
    if obj:
        context = {'detail': obj}
        return render(request, 'main/photo_detail.html', context=context)