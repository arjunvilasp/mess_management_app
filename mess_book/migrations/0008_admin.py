# Generated by Django 5.0.3 on 2024-04-25 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess_book', '0007_remove_student_isadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
