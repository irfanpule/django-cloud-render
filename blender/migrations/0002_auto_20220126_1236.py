# Generated by Django 3.2.9 on 2022-01-26 12:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blender', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user_name',
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fdc73e7e-7fa4-450a-adf8-e3322d97d306'), editable=False, primary_key=True, serialize=False),
        ),
    ]
