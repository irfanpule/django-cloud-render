# Generated by Django 3.2.6 on 2021-08-14 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20210814_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='content',
            field=models.CharField(help_text='Tuliskan jawaban yang akan muncul pada pertanyaan.', max_length=220, verbose_name='Konten'),
        ),
    ]
