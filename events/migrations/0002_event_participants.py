# Generated by Django 4.2.7 on 2023-11-20 11:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='events_participated', to=settings.AUTH_USER_MODEL),
        ),
    ]
