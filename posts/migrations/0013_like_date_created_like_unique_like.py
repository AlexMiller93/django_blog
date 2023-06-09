# Generated by Django 4.1.7 on 2023-03-17 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_post_tags_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 17, 8, 46, 3, 66444, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique_like'),
        ),
    ]
