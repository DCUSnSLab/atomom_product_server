import csv
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

print(os.getcwd())

def insertProductLargeCategory(csvPath):
    from atomom.models import ProductLargeCategory
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            ProductLargeCategory.objects.create( id = row['id'],
                                                 type = row['type'],
                                                 desc = row['desc'], )

def insertProductMediumCategory(csvPath):
    from atomom.models import ProductMediumCategory

    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            ProductMediumCategory.objects.create( id = row['id'],
                                                  type = row['type'],
                                                  desc = row['desc'],
                                                  large_id_id=row['large_id'], )

def insertProductSmallCategory(csvPath):
    from atomom.models import ProductSmallCategory
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            ProductSmallCategory.objects.create(id=row['id'],
                                                 type=row['type'],
                                                 desc=row['desc'],
                                                 medium_id_id=row['medium_id'], )

def insertProduct(csvPath):
    from atomom.models import Product
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            print(row)
            Product.objects.create(id=row['id'],
                                   small_id_id=row['small_id'],
                                   brand=row['brand'],
                                   name=row['name'],
                                   barcode=row['barcode'],)
def insertIngredient(csvPath):
    from atomom.models import Ingredients
    CSV_PATH = csvPath
    with open(CSV_PATH, newline='', encoding="utf-8-sig") as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
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

    csvPath = './data_result.csv'
    insertIngredient(csvPath)
