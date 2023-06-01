# Generated by Django 4.2.1 on 2023-06-01 02:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0010_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='my_app.category')),
            ],
        ),
    ]
