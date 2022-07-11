import csv
import os
import django
from tqdm import tqdm
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# print(os.getcwd())

def insertProductLargeCategory(csvPath):
    from atomom.models import ProductLargeCategory
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            ProductLargeCategory.objects.create( id = row['id'],
                                                 type = row['type'],)

def insertProductMediumCategory(csvPath):
    from atomom.models import ProductMediumCategory

    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            ProductMediumCategory.objects.create( id = row['id'],
                                                  type = row['type'], )

def insertProductSmallCategory(csvPath):
    from atomom.models import ProductSmallCategory
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            ProductSmallCategory.objects.create(id=row['id'],
                                                 type=row['type'],)

def insertProduct(csvPath):
    from atomom.models import Product
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            Product.objects.create(id=row['id'],
                                   brand=row['brand'],
                                   name=row['name'],
                                   subName=row['subName'],
                                   barcode=row['barcode'],)
def insertSubProduct(csvPath):
    from atomom.models import SubProduct
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            SubProduct.objects.create(id=row['id'],
                                   product_id_id=row['product_id'],
                                   subName=row['subName'],
                                   barcode=row['barcode'],)
def PCRelation(csvPath):
    from atomom.models import PCRelation

    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            PCRelation.objects.create(id=row['id'],
                                      product_id_id=row['product_id'],
                                      large_id_id=row['large_id'],
                                      medium_id_id=row['medium_id'],
                                      small_id_id=row['small_id'], )
def SPCRelation(csvPath):
    from atomom.models import SPCRelation

    CSV_PATH = csvPath

    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            SPCRelation.objects.create( id = row['id'],
                                                  subproduct_id_id=row['subproduct_id'],
                                                  large_id_id=row['large_id'],
                                                  medium_id_id=row['medium_id'],
                                                  small_id_id=row['small_id'], )
def insertIngredient(csvPath):
    from atomom.models import Ingredients
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            # print(row)
            Ingredients.objects.create(id=row['id'],
                                      korean=row['korean'].replace('@',','),
                                      oldKorean=row['oldKorean'].replace('@',','),
                                      english=row['English'].replace('@',','),
                                      oldEnglish=row['oldEnglish'].replace('@',','),
                                      hazardScoreMin=row['hazardScoreMin'].replace('@',','),
                                      hazardScoreMax=row['hazardScoreMax'].replace('@',','),
                                      dataAvailability=row['dataAvailability'].replace('@',','),
                                      allergy=row['allergy'].replace('@',','),
                                      twenty=row['twenty'].replace('@',','),
                                      twentyDetail=row['twentyDetail'].replace('@',','),
                                      goodForOily=row['goodForOily'].replace('@',','),
                                      goodForSensitive=row['goodForSensitive'].replace('@',','),
                                      goodForDry=row['goodForDry'].replace('@',','),
                                      badForOily=row['badForOily'].replace('@',','),
                                      badForSensitive=row['badForSensitive'].replace('@',','),
                                      badForDry=row['badForDry'].replace('@',','),
                                      skinRemarkG=row['skinRemarkG'].replace('@',','),
                                      skinRemarkB=row['skinRemarkB'].replace('@',','),
                                      Cosmedical=row['Cosmedical'].replace('@',','),
                                      purpose=row['purpose'].replace('@',','),
                                      limitation=row['limitation'].replace('@',','),
                                      forbidden=row['forbidden'].replace('@',','), )

def insertPIRelation(csvPath):
    from atomom.models import PIRelation
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            PIRelation.objects.create( id = row['id'],
                                       product_id_id=row['product_id'],
                                       ingredients_id_id=row['ingredients_id'],)
def insertSPIRelation(csvPath):
    from atomom.models import SPIRelation
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            SPIRelation.objects.create( id = row['id'],
                                       subproduct_id_id=row['subproduct_id'],
                                       ingredients_id_id=row['ingredients_id'],)



if __name__ == '__main__':
    # csvPath='./tables/Large.csv'
    # insertProductLargeCategory(csvPath)
    # #
    # csvPath = './tables/medium.csv'
    # insertProductMediumCategory(csvPath)
    #
    # csvPath = './tables/small.csv'
    # insertProductSmallCategory(csvPath)
    #
    # csvPath = './tables/product.csv'
    # insertProduct(csvPath)
    #
    # csvPath = './tables/subproduct.csv'
    # insertSubProduct(csvPath)

    # csvPath = './tables/PCRelation.csv'
    # PCRelation(csvPath)

    # csvPath = './tables/SPCRelation.csv'
    # SPCRelation(csvPath)
    #
    # csvPath = './tables/ingredients.csv'
    # insertIngredient(csvPath)

    csvPath = './tables/PIRelation.csv'
    insertPIRelation(csvPath)

    csvPath = './tables/SPIRelation.csv'
    insertSPIRelation(csvPath)


    pass