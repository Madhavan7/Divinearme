# Generated by Django 4.2.2 on 2023-06-13 01:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='temple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('requests_to_join', models.ManyToManyField(related_name='temple_requests', to=settings.AUTH_USER_MODEL)),
                ('temple_location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='search.location')),
                ('temple_members', models.ManyToManyField(related_name='temples', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_date', models.DateField(auto_now_add=True)),
                ('religious_establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.temple')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateField()),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('event_location', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='search.location')),
                ('event_members', models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL)),
                ('religious_establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.temple')),
                ('requests_to_join', models.ManyToManyField(related_name='requested_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='search.post')),
            ],
        ),
        migrations.CreateModel(
            name='temple_invitation',
            fields=[
                ('invitation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.invitation')),
                ('associated_temple', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.temple')),
            ],
            bases=('search.invitation',),
        ),
        migrations.AddField(
            model_name='temple',
            name='invited_users',
            field=models.ManyToManyField(related_name='temple_invitations', through='search.temple_invitation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='event_invitation',
            fields=[
                ('invitation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.invitation')),
                ('associated_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.event')),
            ],
            bases=('search.invitation',),
        ),
        migrations.AddField(
            model_name='event',
            name='invited_users',
            field=models.ManyToManyField(related_name='event_invitations', through='search.event_invitation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='commentReply',
            fields=[
                ('comment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='search.comment')),
                ('parent_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='search.comment')),
            ],
            bases=('search.comment',),
        ),
    ]