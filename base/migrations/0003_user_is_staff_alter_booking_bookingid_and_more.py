# Generated by Django 5.0.3 on 2024-05-27 11:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0002_alter_booking_bookingid_alter_user_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='bookingID',
            field=models.UUIDField(default=uuid.UUID('afad3b2a-a96b-4843-a426-b2aca3392021'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user may belong to multiple groups.', related_name='user_set', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.UUIDField(default=uuid.UUID('28ef9088-6526-45a2-9668-c702c13c6232'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', to='auth.permission'),
        ),
    ]
