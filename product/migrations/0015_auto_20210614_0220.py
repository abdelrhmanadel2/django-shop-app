# Generated by Django 3.2.3 on 2021-06-14 02:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0014_alter_favorite_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dislike',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
