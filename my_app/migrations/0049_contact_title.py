# Generated by Django 3.2.19 on 2024-05-23 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0048_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
