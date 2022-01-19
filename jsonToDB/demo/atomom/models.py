from django.db import models

# Create your models here.

class Product(models.Model): #사람
    id=models.AutoField(help_text="Product ID", primary_key=True,editable=False)
    small_id=models.ForeignKey('ProductSmallCategory', on_delete=models.CASCADE,db_column="small_id")
    brand=models.CharField(help_text="Product Brand", max_length=255, blank=False, null=False)
    name=models.CharField(help_text="Product Name", max_length=255, blank=False, null=False)
    barcode=models.CharField(help_text="Product Barcode", max_length=13, blank=False)
    # sqlite는 varchar에 길이 제약조건이 없네요

class Ingredient:
    pass
class IngredientValue:
    pass
class ewg:
    id=models.AutoField(help_text="ewg ID", primary_key=True,editable=False)


    pass

class ProductLargeCategory(models.Model):
    id = models.AutoField(help_text="Product Large Type ID", blank=False, null=False, primary_key=True)
    type = models.CharField(help_text="Product Large Type Name", max_length=10, blank=False, null=False)
    desc = models.CharField(help_text="Product Large Type Desc", max_length=255, blank=False)

class ProductMediumCategory(models.Model):
    id = models.AutoField(help_text="Product Medium Type ID", blank=False, null=False, primary_key=True)
    type = models.CharField(help_text="Product Medium Type Name", max_length=10, blank=False)
    desc = models.CharField(help_text="Product Medium Type Desc", max_length=255, blank=False)
    large_id = models.ForeignKey('ProductLargeCategory', on_delete=models.CASCADE,db_column="large_id")

class ProductSmallCategory(models.Model):
    id = models.AutoField(help_text="Product Small Type ID", blank=False, null=False, primary_key=True)
    type = models.CharField(help_text="Product Small Type Name", max_length=10, blank=False)
    desc = models.CharField(help_text="Product Small Type Desc", max_length=255, blank=False)
    medium_id = models.ForeignKey('ProductMediumCategory', on_delete=models.CASCADE,db_column="medium_id")

