# Generated by Django 3.2.19 on 2024-05-15 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0029_auto_20240512_2305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='firtsname',
            new_name='firstname',
        ),
    ]
