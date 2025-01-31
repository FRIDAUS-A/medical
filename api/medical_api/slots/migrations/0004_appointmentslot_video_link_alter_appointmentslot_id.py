# Generated by Django 5.1.4 on 2025-01-05 13:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0003_alter_appointmentslot_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentslot',
            name='video_link',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='appointmentslot',
            name='id',
            field=models.CharField(default=uuid.UUID('1fd99e5d-6a87-4831-aa8f-8ac870d8a825'), max_length=50, primary_key=True, serialize=False),
        ),
    ]
