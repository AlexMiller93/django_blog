# Generated by Django 4.1.7 on 2023-03-14 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
