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
                                   barcode=row['barcode'],)
def insertCategoryRelation(csvPath):
    from atomom.models import CategoryRelation

    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in tqdm(data_reader):
            # print(row)
            CategoryRelation.objects.create( id = row['id'],
                                                  product_id_id=row['product_id'],
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
            Ingredients.objects.create(id=row['id'],
                                      korean=row['korean'],
                                      oldKorean=row['oldKorean'],
                                      english=row['English'],
                                      oldEnglish=row['oldEnglish'],
                                      hazardScoreMin=row['hazardScoreMin'],
                                      hazardScoreMax=row['hazardScoreMax'],
                                      dataAvailability=row['dataAvailability'],
                                      allergy=row['allergy'],
                                      twenty=row['twenty'],
                                      twentyDetail=row['twentyDetail'],
                                      goodForOily=row['goodForOily'],
                                      goodForSensitive=row['goodForSensitive'],
                                      goodForDry=row['goodForDry'],
                                      badForOily=row['badForOily'],
                                      badForSensitive=row['badForSensitive'],
                                      badForDry=row['badForDry'],
                                      skinRemarkG=row['skinRemarkG'],
                                      skinRemarkB=row['skinRemarkB'],
                                      Cosmedical=row['Cosmedical'],
                                      purpose=row['purpose'],
                                      limitation=row['limitation'],
                                      forbidden=row['forbidden'], )

if __name__ == '__main__':
    csvPath='./Large.csv'
    insertProductLargeCategory(csvPath)
    #
    csvPath = './medium.csv'
    insertProductMediumCategory(csvPath)

    csvPath = './small.csv'
    insertProductSmallCategory(csvPath)

    csvPath = './product.csv'
    insertProduct(csvPath)

    csvPath = './categoryRelation.csv'
    insertCategoryRelation(csvPath)
    #
    csvPath = './ingredients.csv'
    insertIngredient(csvPath)
    pass