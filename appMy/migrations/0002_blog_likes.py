# Generated by Django 4.2.7 on 2023-12-13 13:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appMy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(related_name='user2', to=settings.AUTH_USER_MODEL, verbose_name='Beğenen Kullanıcılar'),
        ),
    ]
