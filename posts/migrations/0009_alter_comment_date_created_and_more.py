# Generated by Django 4.1.7 on 2023-03-12 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_date_created_alter_post_date_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]