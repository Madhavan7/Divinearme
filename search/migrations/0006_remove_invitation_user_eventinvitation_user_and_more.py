# Generated by Django 4.2.4 on 2023-09-09 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_rename_event_eventpost_eventid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='user',
        ),
        migrations.AddField(
            model_name='eventinvitation',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event_invitations', to='search.usermodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templeinvitation',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='temple_invitations', to='search.usermodel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='invited_users',
            field=models.ManyToManyField(through='search.EventInvitation', to='search.usermodel'),
        ),
        migrations.AlterField(
            model_name='eventinvitation',
            name='associated_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_users_invitations', to='search.event'),
        ),
        migrations.AlterField(
            model_name='temple',
            name='invited_users',
            field=models.ManyToManyField(through='search.TempleInvitation', to='search.usermodel'),
        ),
        migrations.AlterField(
            model_name='templeinvitation',
            name='associated_temple',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invited_users_invitations', to='search.temple'),
        ),
    ]
