# Generated by Django 4.0.4 on 2022-05-14 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_user_gender_user_messages_count_user_profile_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='text_color',
            field=models.CharField(choices=[('lime', 'lime'), ('crimson', 'crimson'), ('cyan', 'cyan')], default='crimson', max_length=20),
        ),
    ]
