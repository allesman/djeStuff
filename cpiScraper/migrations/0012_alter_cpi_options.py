# Generated by Django 4.2.3 on 2023-07-26 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpiScraper', '0011_remove_cpi_name_remove_fatf_name_remove_fsi_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cpi',
            options={'ordering': ['cpi_score'], 'verbose_name_plural': 'CPI'},
        ),
    ]
