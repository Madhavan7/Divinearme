# Generated by Django 4.2.2 on 2023-06-17 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_temple_post_event_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='religious_establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='search.temple'),
        ),
    ]