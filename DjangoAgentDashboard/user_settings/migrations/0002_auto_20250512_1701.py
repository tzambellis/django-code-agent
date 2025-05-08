from django.contrib.auth import get_user_model
from django.db import migrations
from django.utils import timezone


def create_superuser(apps, schema_editor):
    get_user_model().objects.create_superuser(
        username='admin',
        password='admin',
        email='admin@localhost',
        first_name='admin',
        last_name='admin',
        last_login=timezone.now()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('user_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
