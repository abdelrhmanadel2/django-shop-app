# Generated by Django 3.2.3 on 2021-07-05 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20210523_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_provider',
            field=models.CharField(blank=True, default='email', max_length=250, null=True),
        ),
    ]
