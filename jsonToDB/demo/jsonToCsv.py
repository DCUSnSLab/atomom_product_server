# -*- coding: utf-8 -*-
import os, sys
import json
import csv
from tqdm import tqdm
# 매트 립스틱 [칠리]

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

def getIngredient_sub(file):
    pass
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
        if(len(data['Allergy']) != 0): lis[0] = data['Allergy']
        if(len(data['Twenty']) != 0): lis[1] = data['Twenty']
        if(len(data['TwentyDetail']) != 0): lis[2] = data['TwentyDetail']

        if(len(data['Korean']) != 0): lis[3] = data['Korean']
        if(len(data['English']) != 0): lis[4] = data['English']
        if(len(data['Forbidden']) != 0): lis[5] = data['Forbidden']
        if(len(data['Purpose']) != 0): lis[6] = data['Purpose']
        if(len(data['Cosmedical']) != 0): lis[7] = data['Cosmedical']
        if(len(data['Limitation']) != 0): lis[8] = data['Limitation']
        if(len(data['SkinType']) != 0): lis[9] = data['SkinType']
        if(len(data['SkinRemarkB']) != 0): lis[10] = data['SkinRemarkB']
        if(len(data['SkinRemarkG']) != 0): lis[11] = data['SkinRemarkG']
        if(len(data['EWG']) != 0): lis[12] = data['EWG']


        if (len(data['EWG']) != 0):
            if(len(data['EWGDataAvailability']) != 0): lis[13] = data['EWGDataAvailability']
            if(len(data['EWGDataAvailabilityText']) != 0): lis[14]= data['EWGDataAvailabilityText']
        wr,cnt=insertData(wr,cnt,lis)
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

def insertData(wr,cnt,lis=[]):
    if(cnt==1):
        wr.writerow([cnt, 'Allergy', 'Twenty', 'TwentyDetail', 'Korean', 'English',
                     'Forbidden', 'Purpose', 'Cosmedical', 'Limitation', 'SkinType',
                     'SkinRemarkB', 'SkinRemarkG', 'EWG', 'EWGDataAvailability', 'EWGDataAvailabilityText'])
    else:
        wr.writerow([cnt]+lis)
    cnt+=1
    return wr,cnt
    # os.system('pause')
if __name__ == '__main__':
    # sd=" "
    # if(len(sd) != 0): result=sd
    # print(result)
    f = open('data.csv', 'w', newline='')
    wr=csv.writer(f)
    base_path = 'Z:/2021학년도/프로젝트/아토맘/데이터/일반/립메이크업/립스틱\jsonFiles/'
    curList=os.listdir(base_path)
    cnt=1
    wr,cnt=insertData(wr,cnt)
    for i,data in enumerate(curList):
        with open( os.path.join(base_path,data), 'r', encoding='UTF-8-sig') as f:
            curJson=json.load(f)
        print(curJson.keys())
        brand=curJson['brand']
        pName=curJson['productName']

        curJson=curJson['ingredients']
        print(pName,len(curJson))
        ingredient_processing(curJson,wr,cnt)
        # break


    f.close

        # print(curJson)

        # print(curJson[1])


