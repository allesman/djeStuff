from django.shortcuts import render
from django.contrib import admin
from .models import CPI
from .resources import CPIResource
from django_object_actions import DjangoObjectActions
import requests
import tablib

@admin.register(CPI)
class CPIAdmin(DjangoObjectActions,admin.ModelAdmin):
    list_display=('name','cpi_score')
    list_per_page=200
    # list_display=[field.name for field in CPI._meta.fields]
    @admin.action(description='Check for new data')
    def check_for_new_data(self, request, queryset):
        pass
    
    @admin.action(description='Import new data')
    def import_new_data(self, request, queryset):
        # get excel file from url
        r = requests.get('https://www.transparency.de/fileadmin/Redaktion/Aktuelles/2023/CPI2022_Results.xlsx')
        open('CPI2022_Results.xlsx', 'wb').write(r.content)
        new_cpis = open('CPI2022_Results.xlsx', 'rb')
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

    changelist_actions = ('check_for_new_data','import_new_data')


def importExcel(request):
    if request.method=="POST":
        cpi_resource = CPIResource()
        dataset=Dataset()
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