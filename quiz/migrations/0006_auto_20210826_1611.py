# Generated by Django 3.2.6 on 2021-08-26 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_quiz_background_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='background_color',
            field=models.CharField(choices=[('bg-default', 'Coklat'), ('bg-primary', 'Hijau Telur Asin'), ('bg-info', 'Biru Awan'), ('bg-success', 'Hijau Terang'), ('bg-warning', 'Kuning Terang'), ('bg-danger', 'Merah Terang')], default='bg-warning', help_text='Warna yang dipilih akan menjadi warna latar pada quiz ini.', max_length=20, verbose_name='Warna Latar'),
        ),
        migrations.AlterField(
            model_name='question',
            name='button_color',
            field=models.CharField(choices=[('btn-default', 'Coklat'), ('btn-primary', 'Hijau Telur Asin'), ('btn-info', 'Biru Awan'), ('btn-success', 'Hijau Terang'), ('btn-warning', 'Kuning Terang'), ('btn-danger', 'Merah Terang')], default='btn-info', help_text='Warna yang dipilih akan menjadi warna tombol pilihan jawaban pada quiz ini.', max_length=20, verbose_name='Warna Tombol'),
        ),
    ]