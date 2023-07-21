from import_export import resources
from .models import CPI

class CPIResource(resources.ModelResource):
    class Meta:
        model = CPI
        pass