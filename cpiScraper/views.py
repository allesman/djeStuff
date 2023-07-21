from django.shortcuts import render
from django.contrib import admin
from .models import CPI
from tablib import Dataset
from .resources import CPIResource

@admin.register(CPI)
class CPIAdmin(admin.ModelAdmin):
    list_display=[field.name for field in CPI._meta.fields]

def importExcel(request):
    if request.method=="POST":
        cpi_resource = CPIResource()
        dataset=Dataset()
        new_cpis = request.FILES['my_file']
        imported_data = dataset.load(new_cpis.read(),format='xlsx')
        for data in imported_data:
            data=list(data)
            for i in range(len(data)):
                if data[i] == '':
                    data[i] = None
            value = CPI(*data)
            value.save()
    
    return render(request,'form.html')