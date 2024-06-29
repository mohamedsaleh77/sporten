# Generated by Django 5.0.3 on 2024-05-27 11:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_booking_bookingid_alter_user_phone_num_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='bookingID',
            field=models.UUIDField(default=uuid.UUID('7f3ee8ce-82bc-4bc0-8483-209c570a20e3'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.UUIDField(default=uuid.UUID('76111049-5f1c-4115-90a1-4051b3ff058d'), primary_key=True, serialize=False),
        ),
    ]
