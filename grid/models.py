from django.db import models

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


