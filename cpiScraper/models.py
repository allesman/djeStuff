from django.db import models

class CPI(models.Model):
    # Columns for the following data:  Country / Territory	ISO3	Region	CPI score 2022	Rank	Standard error	Number of sources	Lower CI	Upper CI	African Development Bank CPIA	Bertelsmann Foundation Sustainable Governance Index	Bertelsmann Foundation Transformation Index	Economist Intelligence Unit Country Ratings	Freedom House Nations in Transit	Global Insights Country Risk Ratings	IMD World Competitiveness Yearbook	PERC Asia Risk Guide	PRS International Country Risk Guide	Varieties of Democracy Project	World Bank CPIA	World Economic Forum EOS	World Justice Project Rule of Law Index
    name = models.CharField(max_length=100,null=True)
    # iso3 = models.CharField(max_length=3,null=True)
    ## region = models.CharField(max_length=100,null=True)
    cpi_score = models.FloatField(null=True)
    # rank = models.IntegerField(null=True)
    # standard_error = models.FloatField(null=True)
    # number_of_sources = models.IntegerField(null=True)
    # lower_ci = models.FloatField(null=True)
    # upper_ci = models.FloatField(null=True)
    # african_development_bank_cpia = models.FloatField(null=True)
    # bertelsmann_foundation_sustainable_governance_index = models.FloatField(null=True)
    # bertelsmann_foundation_transformation_index = models.FloatField(null=True)
    # economist_intelligence_unit_country_ratings = models.FloatField(null=True)
    # freedom_house_nations_in_transit = models.FloatField(null=True)
    # global_insights_country_risk_ratings = models.FloatField(null=True)
    # imd_world_competitiveness_yearbook = models.FloatField(null=True)
    # perc_asia_risk_guide = models.FloatField(null=True)
    # prs_international_country_risk_guide = models.FloatField(null=True)
    # varieties_of_democracy_project = models.FloatField(null=True)
    # world_bank_cpia = models.FloatField(null=True)
    # world_economic_forum_eos = models.FloatField(null=True)
    # world_justice_project_rule_of_law_index = models.FloatField(null=True)
class FSI(models.Model):
    name = models.CharField(max_length=100,null=True)
    fsi_score = models.FloatField(null=True)
    class Meta:
        # change name of model
        verbose_name_plural = "Overview"
        verbose_name = "Overview"