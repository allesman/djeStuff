# Generated by Django 4.2.3 on 2023-07-26 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpiScraper', '0012_alter_cpi_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cpi',
            options={'ordering': ['-cpi_score'], 'verbose_name_plural': 'CPI'},
        ),
        migrations.AlterModelOptions(
            name='fatf',
            options={'ordering': ['-fatf_score'], 'verbose_name_plural': 'FATF'},
        ),
        migrations.AlterModelOptions(
            name='fsi',
            options={'ordering': ['-fsi_score'], 'verbose_name_plural': 'FSI'},
        ),
        migrations.AlterModelOptions(
            name='overview',
            options={'ordering': ['iso3'], 'verbose_name_plural': 'Overview'},
        ),
    ]