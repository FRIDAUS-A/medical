# Generated by Django 5.1.4 on 2025-01-03 22:16

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slots', '0002_alter_appointmentslot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentslot',
            name='id',
            field=models.CharField(default=uuid.UUID('625daa20-82d3-46ec-a778-267ff72ebb52'), max_length=50, primary_key=True, serialize=False),
        ),
    ]
