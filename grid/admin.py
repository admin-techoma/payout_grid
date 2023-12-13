from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from grid.models import Grid_file,Grid_data,Product,Vehical_Type,Vehical_Sub_Type,Product_Name,Provider,Month,State,Rto

# Register your models here.
admin.site.register(Product)
admin.site.register(Vehical_Type)
admin.site.register(Vehical_Sub_Type)
admin.site.register(Product_Name)
admin.site.register(Provider)
admin.site.register(Month)
admin.site.register(State)
admin.site.register(Rto)
admin.site.register(Grid_file)
admin.site.register(Grid_data)
