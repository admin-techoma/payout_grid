from datetime import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
class Product(models.Model): 

    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Vehical_Type(models.Model):
    product = models.ForeignKey(Product, verbose_name="product", on_delete=models.CASCADE, related_name='vehical_types')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vehical_Sub_Type(models.Model):
    vehical_type = models.ForeignKey(Vehical_Type, verbose_name="vehical_type", on_delete=models.CASCADE, related_name='sub_types')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Product_Name(models.Model):
    vehical_sub_type = models.ForeignKey(Vehical_Sub_Type, verbose_name="vehical_sub_type", on_delete=models.CASCADE, related_name='vehical_sub_type') 
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Provider(models.Model):
    product_name = models.ForeignKey(Product_Name, verbose_name="product", on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Month(models.Model):
    
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class State(models.Model):
    
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Rto(models.Model):
    state = models.ForeignKey(State, verbose_name="state", on_delete=models.CASCADE, related_name='state')
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    

def grid_doc_path(instance,filename):
    return f'grid_files/{filename}'

    #return 'reco_files/{0}'.format(datetime.today())


class Grid_file(models.Model):
    user            = models.CharField(max_length=50,null=True,blank=True)
    created_on      = models.DateField(default=timezone.now)
    uploaded_file   = models.FileField(upload_to=grid_doc_path, default='grid_documents/default.jpg')



class Grid_data(models.Model):

    company         =   models.CharField(max_length=255)             
    product         =   models.CharField(max_length=255)
    vehical_type    =   models.CharField(max_length=255)
    vehical_subtype =   models.CharField(max_length=255)
    product_name    =   models.CharField(max_length=255)
    month           =   models.CharField(max_length=255)
    state           =   models.CharField(max_length=255)
    rto             =   models.CharField(max_length=255)
    rateuser1       =   models.CharField(max_length=255) # Rate user for 70% of requests
    rateuser2       =   models.CharField(max_length=255)# Rate user for 80% of requests
    rateuser3       =   models.CharField(max_length=255)# Rate user for 90% of requests
    remarks         =   models.CharField(max_length=255)
    agent_payout    =   models.CharField(max_length=255)
    created_on      =   models.DateField(default=timezone.now)
    


