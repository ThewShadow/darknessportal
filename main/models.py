import datetime
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    profile_photo = models.ImageField(upload_to='user/images', blank=True)

    gender_choices = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=gender_choices, default='MALE')
    messages_count = models.IntegerField(null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)


    def check_password(self, check_pass):
        return self.password == check_pass

    def __str__(self):
        return f'{self.id} {self.name}'


class Image(models.Model):
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published', null=True, blank=True)
    image = models.ImageField(upload_to='images', verbose_name='path', )

    def save(self, *args, **kwargs):
        if not self.pub_date:
            self.pub_date = datetime.datetime.now()
        return super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.pub_date} - {self.author}'


class Video(models.Model):
    pub_date = models.DateTimeField(verbose_name='date published')
    link = models.CharField(max_length=255)



class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.TimeField()

    def __str__(self):
        return f'{self.author}: {self.text}'


