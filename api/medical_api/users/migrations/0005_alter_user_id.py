# Generated by Django 5.1.4 on 2025-01-05 13:59

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.UUID('59bc8cf2-8951-40c5-b8d2-36c052b3264c'), max_length=50, primary_key=True, serialize=False),
        ),
    ]
