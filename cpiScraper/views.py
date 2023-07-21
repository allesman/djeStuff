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
        for i in range(3,len(imported_data)-1):
            data=list(imported_data[i])
            # for j in range(len(data)):
            #     if data[j] == '':
            #         data[j] = None
            value = CPI(i,data[0],data[3]) #22
            # value = CPI(len(data),"peter")
            value.save()
    
    return render(request,'form.html')