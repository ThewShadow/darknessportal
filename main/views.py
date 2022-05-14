import re
import time
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Image
import datetime
from .models import Video
from django.core import paginator
from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, FormView
from .models import Message
from .models import User
from .forms import ImageForm, NewUserForm, LoginForm, MessageForm, UserForm
from django.contrib.auth import login as login1, authenticate #add this
from django.contrib import messages
from django.forms.models import model_to_dict
import json
from datetime import datetime



class CommonContextMixin:
    def get_common_data(self, request, **kwargs):
        context = kwargs

        new_photos = Image.objects.order_by('-pub_date')[:6]
        new_videos = Video.objects.order_by('-pub_date')[:5]
        messages = Message.objects.order_by('-pub_date')

        context['new_photos'] = new_photos
        context['new_videos'] = new_videos
        context['messages'] = messages
        context['timeformat'] = time.strftime
        context['user_id'] = request.session.get('user_id', 0)
        context['user_name'] = request.session.get('user_name', '')
        context['is_authorizate'] = request.session.get('is_authorizate', False)

        if context['user_id']:
            context['avatar'] = User.objects.get(id=context['user_id']).profile_photo

        return context


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common = self.get_common_data(self.request, **kwargs)
        return dict(list(context.items()) + list(common.items()))



class IndexView(CommonContextMixin, ListView):
    template_name = 'main/index.html'
    model = Video
    context_object_name = 'new_videos'
    success_url = 'dark/'

    def post(self, request):
        text_msg = request.POST.get('user_message')
        usr_id = request.session.get('user_id', 0)
        usr = get_object_or_404(User, id=usr_id)

        text_msg = clear_html_tags(text_msg)

        form = MessageForm({'author': usr, 'text': text_msg, 'pub_date': datetime.now().time()})
        if form.is_valid():
            form.save()
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usr_id = self.request.session.get('user_id', 0)

        try:
            usr = User.objects.get(id=usr_id)
            context['chat_form'] = MessageForm({'author': usr})
        except:
            pass
        return context


class AlbumView(CommonContextMixin, ListView):
    template_name = 'main/album.html'
    model = Image
    context_object_name = 'all'

    def get_queryset(self):
        all_images = Image.objects.order_by('-pub_date')
        pg = paginator.Paginator(all_images, 9)
        page_obj = pg.get_page(self.kwargs.get('page', 1))
        return page_obj


class AddImageView(CommonContextMixin, CreateView):
    template_name = 'main/add_photo.html'
    form_class = ImageForm
    context_object_name = 'form'
    success_url = '/dark/album/list/1'


    def form_valid(self, form):
        id = self.request.session.get('user_id', 0)
        usr = get_object_or_404(User, id=id)
        form.instance.author = usr
        return super().form_valid(form)

    def get_initial(self):
        initial = super(AddImageView, self).get_initial()
        initial['author'] = self.request.session.get('user_name', '')
        return initial

class ImageDetailView(CommonContextMixin, DetailView):
    template_name = 'main/photo_detail.html'
    model = Image
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        common = self.get_common_data(self.request, **kwargs)

        links = make_pagination_links(context['detail'])
        context['prev_link'] = links['prev_link']
        context['next_link'] = links['next_link']

        return dict(list(context.items()) + list(common.items()))

    def get_object(self, queryset=None):
        pk = self.kwargs.get('id', 0)
        return get_object_or_404(Image, pk=pk)



def make_pagination_links(obj):
    prev = None
    next = None
    try:
        prev = Image.objects.filter(~Q(pk=obj.id), pub_date__gte=obj.pub_date)
        prev = prev.order_by('pub_date').first()
    except:
        print('error')

    try:
        next = Image.objects.filter(pub_date__lte=obj.pub_date).exclude(pk=obj.id).order_by('pub_date').last()
    except:
        print('error')

    return dict(prev_link=prev, next_link=next)


def clear_html_tags(html):
    CLEANR = re.compile('<.*?>')
    return re.sub(CLEANR, '', html)

def delete_html_from_data(data):
    for key in data:
        value = data[key.name].data
        if type(value) == str:
            setattr(data[key.name], 'data', clear_html_tags(value))

def register(request):
    if request.method == "POST":
        name = clear_html_tags(request.POST.get('name', ''))
        pswd = clear_html_tags(request.POST.get('password', ''))

        new_user = NewUserForm(dict(name=name, password=pswd))
        try:
            usr = User.objects.get(name=name)
            messages.error(request, 'User exist, try other name')
        except Exception as e:
            if new_user.is_valid():
                new_user.save()
                return redirect(reverse('login'))
            else:
                messages.error(request, message='Data error'+str(e))

    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"form": form})

def login(request):
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            usr = None
            try:
                usr = User.objects.get(name=login_form['name'].value())
            except:
                messages.error(request, 'user not exist')

            if type(usr) == User:
                if usr.check_password(login_form['password'].value()):
                    request.session['is_authorizate'] = True
                    request.session['user_name'] = login_form['name'].value()
                    request.session['user_id'] = usr.id

                    return redirect(reverse('home'))
                else:
                    messages.error(request, 'Permmision Denied: Check correct you data')

    form = LoginForm()
    return render(request=request, template_name="main/login.html", context={"form": form})



def logout(request):
    try:
        del request.session['is_authorizate']
        del request.session['user_name']
        del request.session['user_id']
    except KeyError:
        pass
    return redirect(reverse('home'))

def get_messages(request):

    users_message = Message.objects.order_by('pub_date')[:20]
    usr_id = request.session.get('user_id', '')
    if not usr_id:
        return JsonResponse('[]', safe=False)


    def to_dict(inst):
        return dict(author_name=inst.author.name,
                    text=inst.text,
                    id=inst.author.id,
                    current_id=usr_id,
                    pub_date=str(inst.pub_date),
                    text_color=inst.author.text_color)

    res = list(map(to_dict, list(users_message)))
    return JsonResponse(json.dumps(res), safe=False)

class UserDetail(CommonContextMixin, DetailView):
    template_name = 'main/user_profile.html'
    model = User

    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id', 0)
        return get_object_or_404(User, id=id)


class UserEditDetail(CommonContextMixin, UpdateView):
    template_name = 'main/user_update_profile.html'
    model = User
    #fields = ('name', 'title', 'profile_photo')
    form_class = UserForm
    def get_success_url(self):
        user_id = self.request.session.get('user_id', 0)
        return reverse('user_profile', kwargs={'id':user_id})





