# -*- coding: utf-8 -*-
import os, sys
import json
import csv
import time
import copy
from tqdm import tqdm
# 매트 립스틱 [칠리]
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from atomom.models import Ingredients as idb



def check_renewal(curJson):
    '''
        이거는 리뉴얼된 제품일 경우 안 된 제품과 형태가 다릅니다 따라서 이를 구분해주기 위해 동작합니다
        리뉴얼 제품 매트 립스틱 [칠리]의 경우 4번 정도 리뉴얼이 되어 리뉴얼시 마다 각각 원본 json파일에서 구분되어 있습니다
        이를 확인하는 과정입니다
        제 주석이 이해가 안가실 수도 있기에 예시 json파일 이름을 적어드립니다
        리뉴얼 O
            레트로 매트 립스틱 [707 루비우]
            매트 립스틱 [칠리]
        리뉴얼 X
            크리미 틴트 컬러 밤 인텐스 [11호 벨벳레드]
            레트로 매트 립스틱 [릴렌트리슬리레드]
    '''
    # print(curJson)
    # print(len(curJson), type(curJson))
    # print(type(curJson[0]))
    check = curJson[0]
    if ('ingredients' in check):
        # print('     true', check.keys())
        check = True
    else:
        # print('     false', check.keys())
        check = False
    return check

def getIngredient(file,wr,cnt):
    '''
    Index meaning

    0  : Allergy
    1  : Twenty
    2  : TwentyDetail
    3  : Korean
    4  : English
    5  : Forbidden
    6  : Purpose
    7  : Cosmedical
    8  : Limitation
    9  : SkinType
    10 : SkinRemarkB
    11 : SkinRemarkG
    12 : EWG
    13 : EWGDataAvailability
    14 : EWGDataAvailabilityText
    '''
    lis=[None for i in range(15)]

    for i, data in enumerate(file):
        lis = [None for i in range(15)]
        if(len(data['Allergy']) != 0): lis[0] = data['Allergy'].strip('\"').replace(',','@')
        if(len(data['Twenty']) != 0): lis[1] = data['Twenty'].strip('\"').replace(',','@')
        if(len(data['TwentyDetail']) != 0): lis[2] = data['TwentyDetail'].strip('\"').replace(',','@')

        if(len(data['Korean']) != 0): lis[3] = data['Korean'].strip('\"').replace(',','@')
        # print("\"bek",data['Korean'],"afk",data['Korean'].strip('\"'),"lis[3]",lis[3])
        if(len(data['English']) != 0): lis[4] = data['English'].strip('\"').replace(',','@')
        if(len(data['Forbidden']) != 0): lis[5] = data['Forbidden'].strip('\"').replace(',','@')
        if(len(data['Purpose']) != 0): lis[6] = data['Purpose'].strip('\"').replace(',','@')
        if(len(data['Cosmedical']) != 0): lis[7] = data['Cosmedical'].strip('\"').replace(',','@')
        if(len(data['Limitation']) != 0): lis[8] = data['Limitation'].strip('\"').replace(',','@')
        if(len(data['SkinType']) != 0): lis[9] = data['SkinType'].strip('\"').replace(',','@')
        if(len(data['SkinRemarkB']) != 0): lis[10] = data['SkinRemarkB'].strip('\"').replace(',','@')
        if(len(data['SkinRemarkG']) != 0): lis[11] = data['SkinRemarkG'].strip('\"').replace(',','@')
        if(len(data['EWG']) != 0): lis[12] = data['EWG'].strip('\"').replace(',','@')


        if (len(data['EWG']) != 0):
            if(len(data['EWGDataAvailability']) != 0): lis[13] = data['EWGDataAvailability']
            if(len(data['EWGDataAvailabilityText']) != 0): lis[14]= data['EWGDataAvailabilityText']
        wr,cnt=insertData_ingredients(wr,cnt,lis)
        # os.system('pause')
    # os.system('pause')
    # print('-'*50,'\n\n\n')

def ingredient_processing(curJson,wr,cnt):
    check=check_renewal(curJson)

    if(check==True):
        for i, data in enumerate(curJson):
            # print(type(data),data.keys())
            data=data['ingredients']
            getIngredient(data,wr,cnt)

    else:
        data=curJson
        getIngredient(data,wr,cnt)

def insertData_ingredients(wr,cnt,lis=[]):
    if(cnt==1):
        wr.writerow(['id', 'Allergy', 'Twenty', 'TwentyDetail', 'Korean', 'English',
                     'Forbidden', 'Purpose', 'Cosmedical', 'Limitation', 'SkinType',
                     'SkinRemarkB', 'SkinRemarkG', 'EWG', 'EWGDataAvailability', 'EWGDataAvailabilityText'])
    else:
        wr.writerow([1]+lis)
    cnt+=1
    return wr,cnt
    # os.system('pause')

def getDirPath_sub1(path):
    dirlist=[]
    for filename in os.listdir(path):
        # print(filename)
        if os.path.isdir(os.path.join(path, filename)) == True:
            dirlist.append(os.path.join(path, filename))
    return dirlist

def getDirPath(bashPath):
    resultList=[]
    dirlist = []

    for filename in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, filename)) == True:
            dirlist.append(os.path.join(base_path, filename))
    for path in dirlist:
        # print(path)
        tempList=getDirPath_sub1(path)
        for path2 in tempList:
            tempList2=getDirPath_sub1(path2)

            for path3 in tempList2:
                tempList3 = getDirPath_sub1(path3)
                # print(tempList3)
                resultList+=tempList3
    return resultList

def getDirPath2(bashPath):
    resultList = []
    dirlist = []

    for filename in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, filename)) == True:
            dirlist.append(os.path.join(base_path, filename))


    for path in dirlist:
        # print(path)
        tempList = getDirPath_sub1(path)
        for path2 in tempList:
            tempList2 = getDirPath_sub1(path2)
            for path3 in tempList2:

                # os.system('pause')
                tempList3 = getDirPath_sub1(path3)
                # print(tempList3)
                resultList += tempList3
    return resultList

    # print(dirlist)

def make_ingredients_table(base_path):
    f = open('data_raw.csv', 'w', newline='',encoding='UTF-8-sig')
    wr = csv.writer(f)
    cnt = 1
    wr, cnt = insertData_ingredients(wr, cnt)

    dirList=getDirPath(base_path)
    # print(dirList)
    # for i,data in enumerate(dirList):
    #     print(i,data)
    count=1
    for path in tqdm(dirList):
    # for path in dirList:
    #     if(count<87):
    #         count+=1
    #         continue
        # print(path)
        # path=dirList[39]
        # print(path)
        curList = os.listdir(path)
        # print(curList)

        for i, data in enumerate(curList):
            with open(os.path.join(path, data), 'r', encoding='UTF-8-sig') as f:
                curJson = json.load(f)
            # print(curJson.keys())
            brand = curJson['brand']
            pName = curJson['productName']
            # print(brand,pName)
            curJson = curJson['ingredients']
            # print(path,pName, len(curJson))
            ingredient_processing(curJson, wr, cnt)
            # break
        # break
        f.close

def getCategory_sub(csv_filename,curCategory):
    f = open(csv_filename, 'r', newline='', encoding='UTF-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        id, type = line
        # print(type,curCategory)
        if (type == curCategory):
            curCategory=id
            break
    return curCategory

def getCategory(base_path,cur_path):
    small=""
    medium=""
    large=""
    cur_path=cur_path.replace(base_path,"")
    # print(cur_path)
    cur_path = cur_path.replace("\\jsonFiles", "")
    # print(cur_path)
    large,medium,small=cur_path.split('\\')
    # print(large, medium, small)
    large = large.replace('_', '/')
    medium = medium.replace('_', '/')
    small = small.replace('_', '/')
    # print(large,medium,small)
    small = getCategory_sub('./tables/small.csv', small)
    medium = getCategory_sub('./tables/medium.csv', medium)
    large = getCategory_sub('./tables/large.csv', large)
    # print(large,medium,small)

    # os.system('pause')
    return large,medium,small

def make_product_table(base_path):
    f = open('product_raw.csv', 'w', newline='',encoding='UTF-8-sig')
    wr = csv.writer(f)
    cnt = 1
    # wr, cnt = insertData(wr, cnt)
    product_id=1
    subProduct_id=1
    wr.writerow(['product_id', 'subProduct_id', 'brand', 'name','subName', 'barcode', 'large', 'medium', 'small'])
    dirList=getDirPath2(base_path)
    pathCount=0
    for path in tqdm(dirList):
    # for path in (dirList):
        curList = os.listdir(path)
        large,medium,small=getCategory(base_path,path)
        # if(small!="75"):
        #     # print(small)
        #     continue
        # else:
        #     print(small)
        # print(large,medium,small,'222')
        # os.system('pause')
        for i, data in enumerate(curList):
            with open(os.path.join(path, data), 'r', encoding='UTF-8-sig') as f:
                curJson = json.load(f)
            # print(curJson.keys())
            brand = curJson['brand']
            pName = curJson['productName']
            # print(brand,pName)
            # print(curJson.keys())
            curJson = curJson['ingredients']
            # print(curJson)


            check = check_renewal(curJson)
            if (check == True):
                for i, data in enumerate(curJson):
                    # j = data[0]
                    subName=data['subProductName']
                    # print("name: ",pName,"subName: ",subName)
                    # os.system('pause')

                    # wr.writerow(['id', 'brand', 'name', 'barcode', 'small', 'medium', 'large'])
                    if(i==0):
                        wr.writerow([product_id,-30, brand, pName,subName, None , large, medium, small])
                    else:
                        wr.writerow([product_id,subProduct_id, brand, pName,subName, None, large, medium, small])
                        subProduct_id+=1

                product_id += 1
            else:
                wr.writerow([product_id,-30, brand, pName,None, None , large, medium, small])
                product_id+=1

            # break
        # if(pathCount>3):
        #     break
        # pathCount+=1
        f.close

def make_PIR_table_sub1(file):
    templis = []
    for _, data in enumerate(file):
        templis.append(data['Korean'])
    return templis
def make_PIR_table_sub2(lis):
    # '''
    # 아래껀 db 이용
    # '''
    # resultLis=copy.deepcopy(lis)
    # resultIdLis=copy.deepcopy(lis)
    # for i, data in enumerate(lis):
    #     korean=data
    #     # print("before",korean)
    #
    #     # new[1]=korean
    #     if("(구명칭)" in korean):
    #         # print(korean)
    #         korean=korean.split(';',1)
    #         if(len(korean)>=2):
    #             korean = korean[0]
    #         else:
    #             korean=korean[0].replace('(구명칭)','')
    #     # print("after",korean)
    #     # cur=idb.objects.first().korean
    #     cur = idb.objects.filter(korean__contains  = korean)
    #     id= "ddddd"
    #     text="dddddd"
    #     for data in cur:
    #         # print(data.id,data.korean)
    #         if(data.korean==korean):
    #             resultIdLis[i]=data.id
    #             # resultLis[i]=data.korean
    #             break
    # return resultIdLis
    resultLis = copy.deepcopy(lis)
    resultIdLis = copy.deepcopy(lis)

    for i, data in enumerate(lis):
        korean = data
        # print("before",korean)

        # new[1]=korean
        if ("(구명칭)" in korean):
            # print(korean)
            korean = korean.split(';', 1)
            if (len(korean) >= 2):
                korean = korean[0]
            else:
                korean = korean[0].replace('(구명칭)', '')
        korean = korean.rstrip()
        korean = korean.lstrip()

        # print("after",korean)
        # cur=idb.objects.first().korean
        korean = korean.strip('\"').replace(',', '@')
        f = open("./tables/ingredients.csv", 'r', newline='', encoding='UTF-8-sig')
        rdr = csv.reader(f)
        k = 1
        check = False
        for line in rdr:
            if (k == 1):
                k += 1
                continue
            id = line[0]
            ikorea = line[1].lstrip().rstrip()
            if (ikorea == korean):
                resultIdLis[i] = id
                check = True
                break

        assert check == True, '뭔가 잘못됨\'' + korean + '\'\'' + ikorea + '\'' + str(id)
    # os.system('pause')
    return resultIdLis
    # return re

def make_PIR_table(base_path):
    f = open('PIR_raw2.csv', 'w', newline='', encoding='UTF-8-sig')
    wr = csv.writer(f)
    cnt = 1
    # wr, cnt = insertData(wr, cnt)
    product_id = 1
    subProduct_id = 1
    wr.writerow(['id1','product_id', 'ingredients_id','id2','subproduct_id', 'ingredients_id'])
    dirList = getDirPath2(base_path)
    pathCount = 0
    id=1
    for path in tqdm(dirList):
        # if(cnt<26):
        #     cnt+=1
        #     continue
    # for path in (dirList):
        curList = os.listdir(path)
        # large, medium, small = getCategory(base_path, path)
        for i, data in enumerate(curList):
            # if(product_id<4641):
            #     print("product_id",product_id)
            #     product_id+=1
            #     continue
            with open(os.path.join(path, data), 'r', encoding='UTF-8-sig') as f:
                curJson = json.load(f)
            # print(curJson.keys())

            brand = curJson['brand']
            pName = curJson['productName']
            # print(brand,pName)
            # print(curJson.keys())
            curJson = curJson['ingredients']
            # print(curJson)
            # print(product_id,pName)
            check = check_renewal(curJson)
            if (check == True):
                for i, data in enumerate(curJson):
                    # j = data[0]
                    subName = data['subProductName']
                    # print("name: ",pName,"subName: ",subName)
                    # os.system('pause')

                    # wr.writerow(['id', 'brand', 'name', 'barcode', 'small', 'medium', 'large'])
                    data=data['ingredients']
                    if (i == 0):

                        # print("*" * 80)
                        # print(path,pName)
                        ingredients=make_PIR_table_sub1(data)
                        # print("main",ingredients)
                        tempLis=make_PIR_table_sub2(ingredients)
                        # print(tempLis)
                        for ing_id in tempLis:
                            wr.writerow([id,product_id,ing_id])
                            id+=1
                    else:
                        #여기만 서브
                        # print("*" * 80)
                        # print(path, pName)
                        # print("sub", make_PIR_table_sub1(data))
                        # ingredients = make_PIR_table_sub1(data)
                        # print("main",ingredients)
                        # tempLis = make_PIR_table_sub2(ingredients)
                        # for ing_id in tempLis:
                        #     wr.writerow([300, subProduct_id, ing_id,pName,subName])
                        # wr.writerow([product_id, subProduct_id, brand, pName, subName, None, large, medium, small])
                        # subProduct_id += 1
                        pass

                product_id += 1
            else:
                # print("*"*80)
                # print(path, pName)
                # print("main", make_PIR_table_sub1(curJson))
                ingredients = make_PIR_table_sub1(curJson)
                # print("main",ingredients)
                tempLis = make_PIR_table_sub2(ingredients)
                for ing_id in tempLis:
                    wr.writerow([id, product_id, ing_id])
                    id+=1
                # wr.writerow([product_id, -30, brand, pName, None, None, large, medium, small])
                product_id += 1
            # if(pathCount>3):
            #     break
            # pathCount+=1
            # os.system('pause')
    f.close

def make_SPIR_table(base_path):
    f = open('SPIR_raw.csv', 'w', newline='', encoding='UTF-8-sig')
    wr = csv.writer(f)
    cnt = 1
    # wr, cnt = insertData(wr, cnt)
    product_id = 1
    subProduct_id = 1
    wr.writerow(['id1','product_id', 'ingredients_id','id2','subproduct_id', 'ingredients_id'])
    dirList = getDirPath2(base_path)
    pathCount = 0
    id=1
    for path in tqdm(dirList):
    # for path in (dirList):
        curList = os.listdir(path)
        large, medium, small = getCategory(base_path, path)
        for i, data in enumerate(curList):
            with open(os.path.join(path, data), 'r', encoding='UTF-8-sig') as f:
                curJson = json.load(f)
            # print(curJson.keys())

            brand = curJson['brand']
            pName = curJson['productName']
            # print(brand,pName)
            # print(curJson.keys())
            curJson = curJson['ingredients']
            # print(curJson)

            check = check_renewal(curJson)
            if (check == True):
                for i, data in enumerate(curJson):
                    # j = data[0]
                    subName = data['subProductName']
                    # print("name: ",pName,"subName: ",subName)
                    # os.system('pause')

                    # wr.writerow(['id', 'brand', 'name', 'barcode', 'small', 'medium', 'large'])
                    data=data['ingredients']
                    if (i == 0):
                        # print("*" * 80)
                        # print(path,pName)
                        # ingredients=make_PIR_table_sub1(data)
                        # # print("main",ingredients)
                        # tempLis=make_PIR_table_sub2(ingredients)
                        # for ing_id in tempLis:
                        #     wr.writerow([-300,product_id,ing_id,pName,subName])
                        pass
                    else:
                        #여기만 서브
                        # print("*" * 80)
                        # print(path, pName)
                        # print("sub", make_PIR_table_sub1(data))
                        ingredients = make_PIR_table_sub1(data)
                        # print("main",ingredients)
                        tempLis = make_PIR_table_sub2(ingredients)
                        for ing_id in tempLis:
                            wr.writerow([id, subProduct_id, ing_id])
                            id+=1
                        # wr.writerow([product_id, subProduct_id, brand, pName, subName, None, large, medium, small])
                        subProduct_id += 1

                product_id += 1
            else:
                # print("*"*80)
                # print(path, pName)
                # print("main", make_PIR_table_sub1(curJson))
                # ingredients = make_PIR_table_sub1(curJson)
                # # print("main",ingredients)
                # tempLis = make_PIR_table_sub2(ingredients)
                # for ing_id in tempLis:
                #     wr.writerow([-300, product_id, ing_id,pName,None])
                # # wr.writerow([product_id, -30, brand, pName, None, None, large, medium, small])
                # product_id += 1
                pass
            # if(pathCount>3):
            #     break
            # pathCount+=1
    f.close


if __name__ == '__main__':
    base_path = 'C:/Users/dgdgk/Desktop/ddddd/'
    # make_product_table(base_path)
    make_SPIR_table(base_path)
    # make_ingredients_table(base_path)



    # print(numberToBase(1000, 16))

