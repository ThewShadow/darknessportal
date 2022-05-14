import re

from .models import Image
from django import forms
from django.forms import ModelForm, DateTimeInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from .models import User, Message

class ImageForm(ModelForm):

    class Meta:
        model = Image
        fields = ['author', 'image', 'pub_date']

        widgets = {
            'pub_date': DateTimeInput(attrs={
                'type': 'hidden'
            }),
            'author': TextInput(attrs={
                'type': 'hidden'
            })

        }




class NewUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'password')

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'password')

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = {'author', 'text', 'pub_date'}

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('profile_photo', 'title', 'gender', 'email', 'text_color')


    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.title = clear_html_tags(inst.title)
        inst.email = clear_html_tags(inst.title)
        inst.save()
        return inst

def clear_html_tags(html):
    CLEANR = re.compile('<.*?>')
    return re.sub(CLEANR, '', html)