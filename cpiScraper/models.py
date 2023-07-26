from django.db import models

class CPI(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    cpi_score = models.FloatField(null=True)

class FSI(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    fsi_score = models.FloatField(null=True)

class FATF(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    fatf_score = models.FloatField(max_length=100,null=True)

class Overview(models.Model):
    iso3 = models.CharField(max_length=3,null=True)