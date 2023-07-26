from django.shortcuts import render
from django.contrib import admin
from .models import CPI, FSI, FATF, Overview
from .resources import CPIResource
from django_object_actions import DjangoObjectActions
import requests
import tablib
from django.contrib import messages
import datetime
from . import webscraper
import country_converter as coco
import pandas as pd

# set jahr to current year
jahr = datetime.datetime.now().year
cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{jahr}/CPI{jahr-1}_Results.xlsx'

cc=coco.CountryConverter()

@admin.register(FATF)
class FATFAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('iso3','get_name','fatf_score')
    list_per_page=200
    @admin.display(description='Country')
    def get_name(self, obj):
        return cc.convert(names=obj.iso3, to='name_short')

@admin.register(FSI)
class FSIAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('iso3',"get_name",'fsi_score')
    list_per_page=200
    @admin.display(description='Country')
    def get_name(self, obj):
        return cc.convert(names=obj.iso3, to='name_short')

@admin.register(CPI)
class CPIAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('iso3','get_name','cpi_score')
    list_per_page=200
    @admin.display(description='Country')
    def get_name(self, obj):
        return cc.convert(names=obj.iso3, to='name_short')
    # list_display=[field.name for field in CPI._meta.fields]
    # @admin.action(description='Check for new data')
    # def check_for_new_data(self, request, queryset):
    #     messages.add_message(request, messages.INFO, 'test und so')
    
    # @admin.action(description='Import new data')
    # def import_new_data(self, request, queryset):
    #     # get excel file from url
    #     r = requests.get(cpiURL)
    #     open('CPI2022_Results.xlsx', 'wb').write(r.content)
    #     new_cpis = open('CPI2022_Results.xlsx', 'rb')
    #     # Get the first sheet
    #     imported_data=tablib.Databook()
    #     imported_data.xlsx = new_cpis.read()
    #     imported_data=imported_data.sheets()[0]
    #     # Iterate over the data and save to the database
    #     for i in range(3,len(imported_data)):
    #         # Get the row data
    #         data=list(imported_data[i])
    #         if data[0] is None:
    #             # The first empty row is the end of the data
    #             break
    #         # Create a new CPI object and save it to the database
    #         value = CPI(i,data[0],data[3])
    #         value.save()

    # changelist_actions = ('check_for_new_data','import_new_data')

@admin.register(Overview)
class OverviewAdmin(DjangoObjectActions,admin.ModelAdmin):
    
    list_display=('iso3','get_name','get_cpi_score','get_fsi_score','get_fatf_score')
    list_per_page=300
    @admin.display(description='CPI Score')
    def get_cpi_score(self, obj):
        cpi = CPI.objects.filter(iso3=obj.iso3).first()
        if cpi is None:
            return None
        return cpi.cpi_score
    
    @admin.display(description='FATF Score')
    def get_fatf_score(self, obj):
        fatf = FATF.objects.filter(iso3=obj.iso3).first()
        if fatf is None:
            return None
        return fatf.fatf_score

    @admin.display(description='FSI Score')
    def get_fsi_score(self, obj):
        fsi = FSI.objects.filter(iso3=obj.iso3).first()
        if fsi is None:
            return None
        return fsi.fsi_score
    
    @admin.display(description='Country')
    def get_name(self, obj):
        return cc.convert(names=obj.iso3, to='name_short')

    @admin.action(description='Check for new CPI data')
    def check_for_new_cpi_data(self, request, queryset):
        global jahr
        global cpiURL
        jahr+=1
        cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{jahr}/CPI{jahr-1}_Results.xlsx'
        r = requests.get(cpiURL)
        # check if file exists
        if r.status_code == 200:
            messages.add_message(request, messages.SUCCESS, f'new data exists for {jahr}, click IMPORT NEW CPI DATA to import it')
        else:
            messages.add_message(request, messages.ERROR, f'no new data exists for {jahr}')
            jahr-=1
            cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{jahr}/CPI{jahr-1}_Results.xlsx'
    @admin.action(description='Import new CPI data')
    def import_new_cpi_data(self, request, queryset):
        # delete old data
        CPI.objects.all().delete()
        # get excel file from url
        r = requests.get(cpiURL)
        open('cpi.xlsx', 'wb').write(r.content)
        new_cpis = open('cpi.xlsx', 'rb')
        # Get the first sheet
        imported_data=tablib.Databook()
        imported_data.xlsx = new_cpis.read()
        imported_data=imported_data.sheets()[0]
        # Iterate over the data and save to the database
        for i in range(3,len(imported_data)):
            # Get the row data
            data=list(imported_data[i])
            if data[0] is None:
                # The first empty row is the end of the data
                break
            # Create a new CPI object and save it to the database
            # value = CPI(i,data[0],data[3])
            # value.save()
            iso3=data[1]
            # fix for Kosovo because iso3 from the official(!) dataset is incorrect
            if iso3 == 'KSV':
                iso3 = 'XKX'
            CPI.objects.create(iso3=iso3,cpi_score=data[3])
    
    @admin.action(description='Update FATF lists')
    def update_fatf_lists(self, request, queryset):
        try:
            lists = webscraper.getBothLists()
        except:
            messages.add_message(request, messages.ERROR, 'Error while updating FATF lists')
            return
        # delete old data
        FATF.objects.all().delete()
        # save new data
        for name in lists[0]:
            iso3 = cc.convert(names=name, to='ISO3')
            FATF.objects.create(iso3=iso3,fatf_score=1000)
        for name in lists[1]:
            iso3 = cc.convert(names=name, to='ISO3')
            FATF.objects.create(iso3=iso3,fatf_score=100)
        messages.add_message(request, messages.SUCCESS, 'FATF lists updated')
        # for name in lists[1]:
        #     value = FATF(name,100) # 100 because grey list
        #     value.save()
    
    @admin.action(description="Reset country iso3s")
    def reset_country_iso3s(self, request, queryset):
        Overview.objects.all().delete()
        # combine the country iso3s from cpi, fsi and fatf tables into list, avoiding duplicates
        iso3s = set()
        for cpi in CPI.objects.all():
            iso3s.add(cpi.iso3)
        for fatf in FATF.objects.all():
            iso3s.add(fatf.iso3)
        for fsi in FSI.objects.all():
            iso3s.add(fsi.iso3)
        # # sort iso3s alphabetically
        # iso3s = sorted(iso3s)
        # save the country iso3s to the overview table
        for iso3 in iso3s:
            Overview.objects.create(iso3=iso3)
        # for fatf in FATF.objects.all():
        #     Overview.objects.get_or_create(name=fatf.name)
        # for fsi in FSI.objects.all():
        #     Overview.objects.get_or_create(name=fsi.name)
        # for cpi in CPI.objects.all():
        #     Overview.objects.get_or_create(name=cpi.name)
        # order the overview table by country name reversed
        # Overview.objects.order_by('-iso3')
        messages.add_message(request, messages.SUCCESS, str("Regenerated country iso3s"))

    changelist_actions = ('check_for_new_cpi_data','import_new_cpi_data','update_fatf_lists','reset_country_iso3s')
def importCPI(request):
    if request.method=="POST":
        # cpi_resource = CPIResource()
        # dataset=tablib.Dataset()
        dataset=tablib.Databook()
        new_cpis = request.FILES['my_file']
        # imported_data = dataset.load(new_cpis.read(),format='xlsx')
        # for i in range(0,len(imported_data)-1):
        #     data=list(imported_data[i+3])
        #     if data[0] is None:
        #         break
        #     value = CPI(i,data[0],data[3])
        #     value.save()
        #     # value=CPI(imported_data[i])
        # Get the first sheet
        # imported_data.xlsx = new_cpis.read()
        # imported_data=imported_data.sheets()[0]
        imported_data = dataset.load(new_cpis.read(),format='xlsx').sheets()[0]
        # Iterate over the data and save to the database
        for i in range(3,len(imported_data)):
            # Get the row data
            data=list(imported_data[i])
            if data[0] is None:
                # The first empty row is the end of the data
                break
            iso3=data[1]
            # fix for Kosovo because iso3 from the official(!) dataset is incorrect
            if iso3 == 'KSV':
                iso3 = 'XKX'
            CPI.objects.create(iso3=iso3,cpi_score=data[3])
            # value = CPI(i,data[0],data[3])
            # value.save()
    return render(request,'form.html')

def importFSI(request):
    if request.method=="POST":
        # dataset=tablib.Dataset()
        dataset=tablib.Databook()
        new_fsis = request.FILES['my_file']
        imported_data = dataset.load(new_fsis.read(),format='xlsx').sheets()[0]
        for i in range(0,len(imported_data)):
            data=list(imported_data[i])
            if data[0] is None:
                break
            iso3 = cc.convert(names=data[1], to='ISO3')
            FSI.objects.create(iso3=iso3,fsi_score=data[5])
            # value = FSI(i,data[0],data[3])
            # value=FSI(i,data[1],data[5])
            # value.save()
    return render(request,'form.html')