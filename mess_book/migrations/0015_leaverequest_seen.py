# Generated by Django 5.0.3 on 2024-04-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_book', '0014_leaverequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='seen',
            field=models.IntegerField(default=0),
        ),
    ]
