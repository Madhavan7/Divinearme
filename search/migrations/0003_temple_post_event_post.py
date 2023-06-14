# Generated by Django 4.2.2 on 2023-06-14 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_alter_event_event_members_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='temple_post',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.post')),
                ('temple', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='search.temple')),
            ],
            bases=('search.post',),
        ),
        migrations.CreateModel(
            name='event_post',
            fields=[
                ('post_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.post')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='search.event')),
            ],
            bases=('search.post',),
        ),
    ]
