# Generated by Django 4.1.7 on 2023-03-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_rename_comment_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=140, null=True),
        ),
    ]
