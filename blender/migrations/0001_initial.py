# Generated by Django 3.2.9 on 2021-11-09 01:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('09c42149-1c80-427d-8835-a2b482673c92'), editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Project Name')),
                ('file', models.FileField(upload_to='', verbose_name='Blender File')),
                ('user_name', models.CharField(blank=True, help_text='optional', max_length=255, null=True, verbose_name='Your Name')),
            ],
        ),
        migrations.CreateModel(
            name='RenderResult',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('d8197b1c-6d82-40fe-a166-6be21b373fe4'), editable=False, primary_key=True, serialize=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='blender.project')),
            ],
        ),
    ]