# Generated by Django 4.2.3 on 2023-07-21 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpiScraper', '0004_remove_cpi_num_sources_remove_cpi_std_error_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cpi',
            name='african_development_bank_cpia',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='bertelsmann_foundation_sustainable_governance_index',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='bertelsmann_foundation_transformation_index',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='economist_intelligence_unit_country_ratings',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='freedom_house_nations_in_transit',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='global_insights_country_risk_ratings',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='imd_world_competitiveness_yearbook',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='iso3',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='lower_ci',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='number_of_sources',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='perc_asia_risk_guide',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='prs_international_country_risk_guide',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='region',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='standard_error',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='upper_ci',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='varieties_of_democracy_project',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='world_bank_cpia',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='world_economic_forum_eos',
        ),
        migrations.RemoveField(
            model_name='cpi',
            name='world_justice_project_rule_of_law_index',
        ),
    ]