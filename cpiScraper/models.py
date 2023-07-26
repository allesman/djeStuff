from django.db import models

class CPI(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    cpi_score = models.FloatField(null=True)
    class Meta:
        ordering = ['-cpi_score']
        verbose_name_plural = "CPI"

class FSI(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    fsi_score = models.FloatField(null=True)
    class Meta:
        ordering = ['-fsi_score']
        verbose_name_plural = "FSI"

class FATF(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    fatf_score = models.FloatField(max_length=100,null=True)
    class Meta:
        ordering = ['-fatf_score']
        verbose_name_plural = "FATF"

class Overview(models.Model):
    iso3 = models.CharField(max_length=3,null=True)
    class Meta:
        ordering = ['iso3']
        verbose_name_plural = "Overview"
    def __str__(self):
        return self.iso3