# Generated by Django 5.0.3 on 2024-04-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_book', '0005_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]
