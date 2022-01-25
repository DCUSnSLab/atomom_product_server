from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Product(models.Model): #사람
    id=models.AutoField(help_text="Product ID", primary_key=True,editable=False)
    small_id=models.ForeignKey('ProductSmallCategory', on_delete=models.CASCADE,db_column="small_id")
    brand=models.CharField(help_text="Product Brand", max_length=255, blank=False, null=False)
    name=models.CharField(help_text="Product Name", max_length=255, blank=False, null=False)
    barcode=models.CharField(help_text="Product Barcode", max_length=13, blank=False)
    # sqlite는 varchar에 길이 제약조건이 없네요

class Ingredients(models.Model):
    id = models.AutoField(help_text="Ingredient ID", primary_key=True, editable=False)
    korean = models.CharField(help_text="Product Brand", max_length=3024, blank=False, null=False)
    oldKorean = models.CharField(help_text="Product Brand", max_length=3024, blank=False, null=True)
    english = models.CharField(help_text="Product Brand", max_length=3024, blank=False, null=True)
    oldEnglish = models.CharField(help_text="Product Brand", max_length=3024, blank=False, null=True)
    # hazardScoreMin = models.IntegerField(help_text="Product Brand", validators=[MaxValueValidator(10), MinValueValidator(1)], blank=False, null=True)
    # hazardScoreMax = models.IntegerField(help_text="Product Brand",validators=[MaxValueValidator(10), MinValueValidator(1)], blank=False, null=True)
    hazardScoreMin = models.CharField(help_text="Product Brand", max_length=2, blank=False, null=True)
    hazardScoreMax = models.CharField(help_text="Product Brand", max_length=2, blank=False, null=True)
    dataAvailability = models.CharField(help_text="Product Brand", max_length=20, blank=False, null=True)
    allergy = models.CharField(help_text="Product Brand", max_length=1, blank=False, null=True)
    twenty = models.CharField(help_text="Product Brand", max_length=255, blank=False, null=True)
    twentyDetail = models.CharField(help_text="Product Brand", max_length=255, blank=False, null=True)
    goodForOily = models.BooleanField(default=False)
    goodForSensitive = models.BooleanField(default=False)
    goodForDry = models.BooleanField(default=False)
    badForOily = models.BooleanField(default=False)
    badForSensitive = models.BooleanField(default=False)
    badForDry = models.BooleanField(default=False)
    skinRemarkG = models.CharField(help_text="Product Brand", max_length=50, blank=False, null=True)
    skinRemarkB = models.CharField(help_text="Product Brand", max_length=50, blank=False, null=True)
    Cosmedical = models.CharField(help_text="Product Brand", max_length=50, blank=False, null=True)
    purpose = models.CharField(help_text="Product Brand", max_length=512, blank=False, null=True)
    limitation = models.CharField(help_text="Product Brand", max_length=512, blank=False, null=True)
    forbidden = models.CharField(help_text="Product Brand", max_length=512, blank=False, null=True)



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

