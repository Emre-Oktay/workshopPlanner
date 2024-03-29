# Generated by Django 4.2.7 on 2023-12-06 03:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_alter_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsessionitem',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='events.event'),
        ),
    ]
