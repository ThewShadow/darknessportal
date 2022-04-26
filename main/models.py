from django.db import models


class Image(models.Model):
    author = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')
    image = models.ImageField(upload_to='images', verbose_name='path')

    def __str__(self):
        return f'{self.id} - {self.pub_date} - {self.author}'


class Video(models.Model):
    pub_date = models.DateTimeField(verbose_name='date published')
    link = models.CharField(max_length=255)
