from django.shortcuts import render
from django.contrib import admin
from .models import CPI, FSI
from .resources import CPIResource
from django_object_actions import DjangoObjectActions
import requests
import tablib
from django.contrib import messages
import datetime

# set jahr to current year
jahr = datetime.datetime.now().year
cpiURL = f'https://www.transparency.de/fileadmin/Redaktion/Aktuelles/{jahr}/CPI{jahr-1}_Results.xlsx'

@admin.register(CPI)
class CPIAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('name','cpi_score')
    list_per_page=200
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

@admin.register(FSI)
class FSIAdmin(DjangoObjectActions,admin.ModelAdmin):
    
    list_display=('name','get_cpi_score','fsi_score')
    list_per_page=300
    @admin.display(description='CPI Score')
    def get_cpi_score(self, obj):
        cpi = CPI.objects.filter(name=obj.name).first()
        if cpi is None:
            return None
        return cpi.cpi_score
    
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
            value = CPI(i,data[0],data[3])
            value.save()

    changelist_actions = ('check_for_new_cpi_data','import_new_cpi_data')
def importCPI(request):
    if request.method=="POST":
        cpi_resource = CPIResource()
        dataset=tablib.Dataset()
        new_cpis = request.FILES['my_file']
        imported_data = dataset.load(new_cpis.read(),format='xlsx')
        for i in range(0,len(imported_data)-1):
            data=list(imported_data[i+3])
            if data[0] is None:
                break
            value = CPI(i,data[0],data[3])
            value.save()
            # value=CPI(imported_data[i])
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
            # value = FSI(i,data[0],data[3])
            value=FSI(i,data[1],data[5])
            value.save()
    return render(request,'form.html')