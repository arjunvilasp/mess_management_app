# Generated by Django 5.0.3 on 2024-05-02 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_book', '0032_complaint_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='admin_seen',
            field=models.IntegerField(default=0),
        ),
    ]
