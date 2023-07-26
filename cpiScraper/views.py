from django.shortcuts import redirect, render
from django.contrib import admin
from .models import CPI, FSI, FATF, Overview
from django_object_actions import DjangoObjectActions
import requests
import tablib
from django.contrib import messages
import datetime
from . import webscraper
import country_converter as coco

# changes the year for the cpi data, updating the url
def setYear(value):
    global year
    global cpiURL
    year = value
    cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{year}/CPI{year-1}_Results.xlsx'

# set year to current year
year=int()
setYear(datetime.datetime.now().year)

# create country converter object for faster country name conversion
cc=coco.CountryConverter()


# SIMPLE VIEWS FOR THE THREE SCORE TABLES

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


# VIEW FOR THE OVERVIEW TABLE
# combines the three score tables and offering some actions to update the data

@admin.register(Overview)
class OverviewAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('iso3','get_name','get_cpi_score','get_fsi_score','get_fatf_score')
    list_per_page=300

    # admin display functions to get the country name and the scores from the other tables 

    @admin.display(description='Country')
    def get_name(self, obj):
        return cc.convert(names=obj.iso3, to='name_short')
    
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

    # admin actions to update the data

    @admin.action(description="Reset country iso3s")
    def reset_iso3s(self, request, queryset):
        Overview.objects.all().delete()
        # combine the country iso3s from cpi, fsi and fatf tables into set, avoiding duplicates
        iso3s = set()
        for model in [CPI, FSI, FATF]:
            for obj in model.objects.all():
                iso3s.add(obj.iso3)
        # save the country iso3s to the overview table
        for iso3 in iso3s:
            Overview.objects.create(iso3=iso3)
        # show success message
        messages.add_message(request, messages.SUCCESS, str("Regenerated country iso3s"))

    @admin.action(description='Check for new CPI data')
    def check_for_new_cpi_data(self, request, queryset):
        # increment year
        setYear(year+1)
        # get file from url for this new year
        r = requests.get(cpiURL)
        # check if file exists
        if r.status_code == 200:
            # show success message
            messages.add_message(request, messages.SUCCESS, f'new data exists for {year}, click IMPORT NEW CPI DATA to import it')
        else:
            # show error message
            messages.add_message(request, messages.ERROR, f'no new data exists for {year}')
            # reset year to previous year
            setYear(year-1)

    @admin.action(description='Import new CPI data')
    def update_cpi(self, request, queryset):
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
            # get iso3 from table
            iso3=data[1]
            # fix for Kosovo because iso3 from the official(!) dataset is incorrect
            if iso3 == 'KSV':
                iso3 = 'XKX'
            # create new entry in database
            CPI.objects.create(iso3=iso3,cpi_score=data[3])
        # show success message
        messages.add_message(request, messages.SUCCESS, f'new data imported for {year}')
    
    @admin.action(description='Update FSI data')
    def update_fsi(self, request, queryset):
        # since the FSI data needs an account to download, we can't automate this
        # so we just open the /importFSI page, where the user can upload the data manually
        return redirect('/importFSI')

    @admin.action(description='Update FATF lists')
    def update_fatf(self, request, queryset):
        # try to get the lists from the website via webscraper
        try:
            lists = webscraper.getBothLists()
        except:
            # show error message
            messages.add_message(request, messages.ERROR, 'Error while updating FATF lists')
            return
        # delete old data
        FATF.objects.all().delete()
        # save new data
        # score 1000 for blacklist, 100 for greylist
        for name in lists[0]:
            iso3 = cc.convert(names=name, to='ISO3')
            FATF.objects.create(iso3=iso3,fatf_score=1000)
        for name in lists[1]:
            iso3 = cc.convert(names=name, to='ISO3')
            FATF.objects.create(iso3=iso3,fatf_score=100)
        # show success message
        messages.add_message(request, messages.SUCCESS, 'FATF lists updated')

    # add all actions to admin page
    changelist_actions = ('reset_iso3s','check_for_new_cpi_data','update_cpi','update_fsi','update_fatf')


# VIEWS FOR THE IMPORT PAGES
# here, the user can upload the data manually

# this view is needed to manually update the FSI data, as this is the only way to get the data
def importFSI(request):
    if request.method=="POST":
        dataset=tablib.Databook()
        new_fsis = request.FILES['my_file']
        imported_data = dataset.load(new_fsis.read(),format='xlsx').sheets()[0]
        for i in range(0,len(imported_data)):
            data=list(imported_data[i])
            if data[0] is None:
                break
            iso3 = cc.convert(names=data[1], to='ISO3')
            FSI.objects.create(iso3=iso3,fsi_score=data[5])
    return render(request,'fsiForm.html')

# this view should never be needed, as the data is updated via admin actions
# however, if the automatic update fails, this view can be used to manually update the data
def importCPI(request):
    if request.method=="POST":
        # cpi_resource = CPIResource()
        # dataset=tablib.Dataset()
        dataset=tablib.Databook()
        new_cpis = request.FILES['my_file']
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
    return render(request,'cpiForm.html')
