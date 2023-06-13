# Generated by Django 4.2.2 on 2023-06-13 03:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_members',
            field=models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='requests_to_join',
            field=models.ManyToManyField(blank=True, related_name='requested_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='temple',
            name='requests_to_join',
            field=models.ManyToManyField(blank=True, related_name='temple_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='temple',
            name='temple_members',
            field=models.ManyToManyField(blank=True, related_name='temples', to=settings.AUTH_USER_MODEL),
        ),
    ]
