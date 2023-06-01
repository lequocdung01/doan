from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0009_auto_20230531_1211'),
    ]

    operations = [
        migrations.DeleteModel(
            name='category',
        ),
    ]
