import os
import time

import django
from cdifflib import CSequenceMatcher
import difflib
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from atomom.models import Product
from tqdm import tqdm
def getChunk(lis):
    lens=[[i+1,None] for i in range(90)]
    lens=dict(lens)
    # print(lens)

    start=1
    startIdx=0
    for i, data in enumerate(lis):
        length=len(data)
        if(length==start):
            if(len(lis)==i+1):
                lens[start] = (startIdx, i - 1)
        elif(length>=start):
            lens[start]=(startIdx,i-1)
            start=start+1
            startIdx=i

    # print(lis)
    # print(lens)
    # print((lens[1]))
    # print(lis[22])
    # print(lis[23])
    return lens


def compData_chunk(cur,lenDict,target,score=70):
    targetIndex=len(target)
    targetRange=(int(targetIndex*0.5),int(targetIndex*1.5))
    difflib.SequenceMatcher = CSequenceMatcher
    seq = difflib.SequenceMatcher()
    seq.set_seq1(target)
    check=False
    resultList=[]
    maxRatio=0
    t1=time.time()
    cnt=0
    # print(target)
    # print("     ",targetIndex)
    # print("     ",targetRange)
    if(targetRange[0]==0):
        return compData_full(cur,target,score)
    for i in range(targetRange[0],targetRange[1]+1):
        index=lenDict[i]
        # print(index)
        for idx in range(index[0],index[1]+1):
            seq.set_seq2(cur[idx])
            cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
            # cur_ratio = (lambda x: seq.ratio() * 100)(0)
            cnt+=1
            if(cur_ratio>=maxRatio):
                resultList.append((idx,cur[idx],cur_ratio))
                maxRatio=cur_ratio
            if(cur_ratio>score):
                check=True
                break
        if(check==True):
            break
    # print(cnt)
    return resultList
def compData_full(cur,target,score=90):
    difflib.SequenceMatcher = CSequenceMatcher



    seq = difflib.SequenceMatcher()
    seq.set_seq1(target)
    maxValue=0
    result_list=[]

    for i, data in enumerate(cur):
        seq.set_seq2(data)
        cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
        if(maxValue<=cur_ratio):
            result_list.append((i,data,cur_ratio))
            maxValue=cur_ratio
        if(cur_ratio>90):
            break
    return result_list
import csv
def equals(s1,s2):
    if(s1==s2):
        return True
    else:
        return False
def exp(cnt,cur,lenDict,score=90):
    fr = open('./experiment/experiment_'+str(cnt) + '.csv', 'r', newline='', encoding='UTF-8-sig')
    rdr = csv.reader(fr)
    lis=list(rdr)

    dataList=[]
    count=1
    for i in lis:
        origin=i[0]
        target=i[1]
        t1=time.time()
        a=compData_chunk(cur,lenDict,target=target,score=score)
        t1=time.time()-t1
        t2=time.time()
        b=compData_full(cur,target=target,score=score)
        t2=time.time()-t2
        data=[origin,target,b[len(b) - 1][1],a[len(a) - 1][1],
              equals(origin,b[len(b) - 1][1]),equals(origin,a[len(a) - 1][1]),
              b[len(b) - 1][2],a[len(a) - 1][2],
              t2,t1
              ]
        # print(data)
        # print("         ", b[len(b) - 1])
        # print("         ", a[len(a) - 1])
        # os.system('pause')
        dataList.append(data)
        if(count>=1000):
            break
        count+=1
    # print(dataList)
        # assert b[len(b) - 1][2] == a[len(a) - 1][2], "다르네요 "
    return dataList
def experiments(cur,lenDict,score=90):
    wb, ws = setSheet()

    resultRow, resultCol = (7, 3)

    formatList = ['origin', 'converted', 'full_result', 'chunk_result',
                  'same_full', 'same_chunk', 'full_similarity',
                  'chunk_similarity', 'full_time', 'chunk_time']

    resultFormat = ['levenshetin', 'full_avg_time', 'chunk_avg_time',
                    'full_avg_similarity','chunk_avg_similarity',
                    'nText','full_same_count','chunk_same_count',
                    'full_match_rate','chunk_match_rate'
                    ]

    rWs = wb['result']
    rWs = excel.makeFormat(rWs, resultRow, resultCol, resultFormat)
    resultRow += 1

    for cnt in tqdm(range(1,11)):
        sheetRow, sheetCol = (7, 3)
        ws = wb[str(cnt)]
        ws = excel.makeFormat(ws, sheetRow, sheetCol, formatList)
        sheetRow+=1
        # sheetRow+=1
        dataList=exp(cnt, cur, lenDict, score=score)
        full_avg_time = 0
        chunk_avg_time = 0
        full_avg_similarity = 0
        chunk_avg_similarity = 0
        full_same_count = 0
        chunk_same_count = 0
        divide=0
        for i in range(len(dataList)):
            ws = excel.writeData2(ws, sheetRow, sheetCol, dataList[i])
            sheetRow += 1
            full_avg_time += dataList[i][8]
            chunk_avg_time += dataList[i][9]
            full_avg_similarity += dataList[i][6]
            chunk_avg_similarity += dataList[i][7]

            if (dataList[i][4] == True):
                full_same_count += 1
            if (dataList[i][5] == True):
                chunk_same_count += 1
            divide += 1
        resultData=[cnt,full_avg_time/divide,chunk_avg_time/divide,
                    full_avg_similarity/divide,chunk_avg_similarity/divide,
                    divide,full_same_count,chunk_same_count,
                    full_same_count/divide*100,chunk_same_count/divide*100
                    ]
        rWs = excel.writeData2(rWs, resultRow, resultCol, resultData)
        resultRow+=1
        excel.excelSave(wb, "./experiment/", "result")

    pass

from etc import excelExport as excel
def setSheet():
    wb, ws = excel.makeWb()
    for i in range(1, 11, 1):
        if (i == 1):
            ws.title = str(i)
        else:
            ws = wb.create_sheet()
            ws.title = str(i)

    ws = wb.create_sheet()
    ws.title = "result"
    return wb,ws

if __name__ == '__main__':
    te=list(Product.objects.all().values_list('name', flat=True))
    # print(te[0])
    cur = sorted(list(Product.objects.all().values_list('name', flat=True)),key=len)

    # print(cur)

    lenDict=getChunk(cur)
    print(cur[153159])
    print(lenDict)
    # target="닥터지 레드 블레미쉬 클리어 수딩 크림 moistunz"
    # # target = "레드 블레미쉬 클리어 수딩 크림"
    # t1=time.time()
    # result=compData_chunk(cur,lenDict,target,score=90)
    # t1=time.time()-t1
    # print(t1, result[len(result)-1])
    # t2=time.time()
    # compData_full(cur,target)
    # t2=time.time()-t2
    # print(t2, result[len(result)-1])
    # experiments(cur,lenDict,score=95)



