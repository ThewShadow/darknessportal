# Generated by Django 4.0.4 on 2022-05-08 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_user_email_user_password1_user_password2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='password1',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password2',
        ),
    ]
