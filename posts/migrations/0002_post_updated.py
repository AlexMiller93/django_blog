# Generated by Django 4.1.6 on 2023-02-13 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
