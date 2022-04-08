from cdifflib import CSequenceMatcher
import difflib
import numpy as np
import copy
import time
import copy
import os
import time

import django
from django.db.models import Q
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
print(os.getcwd())
from atomom.models import Product
from tqdm import tqdm
from numba import jit


def getChunk_(lis):
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
            print(i, data,startIdx,len(data))
            lens[start]=(startIdx,i-1)
            start=start+1
            startIdx=i
    return lens

# @jit(nopython=True)
def __getLenghDict(lis,resultList):

    for i,data in enumerate(lis):
        resultList[i]=int(len(data))
    # print(resultList)
    resultList = sorted(list(set(resultList)), key=int)
    lenDict = dict([[i, None] for i in resultList])
    return lenDict

def getChunk(lis):
    import numpy as np
    import time
    lis=np.array(lis)
    # print(lis.dtype,"dd")
    t1=time.time()
    lenDict=__getLenghDict(lis,lis.copy())
    # print(time.time()-t1)
    # print(lenDict)
    keys=lenDict.keys()
    keyList=sorted(keys,key=int)
    # print(keys)
    # print(type(keys))
    # print(keyList)
    # print(lenDict)
    startIdx=0
    # print(len(lis))
    for key in keyList:
        count=0
        # print("key=",key)
        for i in range(startIdx,len(lis)):
            # print(lis[i],len(lis[i]),key)
            if(len(lis[i])!=int(key)):
                # print(lis[i],len(lis[i]),key)
                break
            else:
                # print("여기")
                count+=1

        # print((startIdx,count))
        # print(lenDict['1'])

        # print(startIdx,count)
        lenDict[key]=(startIdx,startIdx+count)
        startIdx=startIdx+count

        # os.system('pause')
        # print(lis[startIdx],lis[startIdx+count])
        # print("startIdx",startIdx)
    # print(lenDict)
    # for i in lenDict:
    #     print(lenDict[str(i)])

        # break
    # for i, data in enumerate(lis):
    #     print(i,data)
    return lenDict





def compData_chunk(cur,lenDict,target,score,includeBrandKor=False,includeBrandEng=False):
    if (len(target) == 0):
        return [(None, (None, None), 0)]
    targetIndex=len(target)
    targetRange=(int(targetIndex*0.5),int(targetIndex*1.5))

    temp=[i for i in range(targetRange[0],targetRange[1]+1)]
    # temp = [i for i in range(targetRange[0], targetRange[1] + 101)]
    targetRange=copy.deepcopy(temp)
    # print(target,len(target),targetRange)
    # print("targetRange",targetRange)
    for i in range(len(temp)):
        # print(temp[i],type(temp[i]))
        if str(temp[i]) in lenDict:
            # print("있네요",temp[i])
            pass
        else:
            # print("targetRange",targetRange)
            # print("temp[i]",temp[i])
            targetRange.remove(temp[i])

        # os.system('pause')
    # print(targetRange)

    # os.system('pause')
    difflib.SequenceMatcher = CSequenceMatcher
    seq = difflib.SequenceMatcher()
    seq.set_seq1(target)
    check=False
    resultList=[]
    maxRatio=0
    t1=time.time()
    cnt=0

    for i in targetRange:
        index=lenDict[str(i)]
        # print(index)
        # print(index)
        # for idx in range(index[0],index[1]+1):
        for idx in range(index[0], index[1]):
            brandKor=''
            brandEng=''
            # print("cur[idx]",cur[idx])
            # print("len(cur)",len(cur),"idx",idx)
            # print("cur[idx]",cur[idx],'\n\n')
            if('(' in cur[idx][2]):
                brand=cur[idx][2].split('(')
                brandKor=brand[0]
                brandEng=brand[1].split(')')[0]
            else:
                brandKor=cur[idx][2]
                brandEng=cur[idx][2]

            if(includeBrandKor==True):
                # print(type(brandKor),cur[idx][2],brandKor)
                seq.set_seq2(brandKor+cur[idx][1])
            elif (includeBrandEng == True):
                seq.set_seq2(brandEng + cur[idx][1])
            else:
                seq.set_seq2(cur[idx][1])

            cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
            # cur_ratio = (lambda x: seq.ratio() * 100)(0)
            cnt+=1
            if(cur_ratio>=maxRatio):
                resultList.append((idx,cur[idx],cur_ratio))
                maxRatio=cur_ratio
            if(cur_ratio>=score):
                check=True
                break
        if(check==True):
            break
    # print(cnt)
    return resultList
def compData_full(cur,target,score=90,includeBrandLeft=False,includeBrandRight=False):
    if (len(target) == 0):
        return [(None, (None,None), 0)]
    difflib.SequenceMatcher = CSequenceMatcher

    seq = difflib.SequenceMatcher()
    seq.set_seq1(target)
    maxValue=0
    result_list=[]
    brandLeft=""
    brandRight=""
    for i, data in enumerate(cur):
        compTarget=data[1]
        if(includeBrandLeft == True or includeBrandRight == False):
            if ('(' in data[2]):
                brand = data[2].split('(')
                brandLeft = brand[0].strip()+' '
                brandRight = brand[1].split(')')[0].strip()+' '
            else:
                brandLeft = data[2].strip()+' '
                brandRight = data[2].strip()+' '

            if (includeBrandLeft == True):
                compTarget=brandLeft + data[1]
            elif (includeBrandRight == True):
                compTarget=brandRight + data[1]

        seq.set_seq2(compTarget)
        cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
        if(maxValue<=cur_ratio):
            result_list.append((i,data,cur_ratio))
            maxValue=cur_ratio
        if(cur_ratio>=score):
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
        # print("***"*50)
        # print("a\n",a)
        # print("b\n", b)
        #
        data=[origin,target,b[len(b) - 1][1][1],a[len(a) - 1][1][1],
              equals(origin,b[len(b) - 1][1][1]),equals(origin,a[len(a) - 1][1][1]),
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
def experiments(cur,lenDict,score=95):
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
            # if(type(dataList[i][6]) != type(None)): full_avg_similarity += dataList[i][6]
            # if(type(dataList[i][7]) != type(None)): chunk_avg_similarity += dataList[i][7]
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
    target="안녕ㅇ"
    compT="안녕"
    difflib.SequenceMatcher = CSequenceMatcher

    seq = difflib.SequenceMatcher()
    seq.set_seq1(target)
    maxValue = 0
    result_list = []

    seq.set_seq2(compT)
    print(seq.quick_ratio() * 100)
    # id=106151
    # query=Product.objects.raw('select * from atomom_ingredients where id IN (select ingredients_id from atomom_pirelation where product_id=%s)',[id])
    # for q in query:
    #     print(q.korean)
    ocrR=['멀티', '유즈','아이팔레트','스타티스']
    q = Q()
    for i in ocrR:
        q.add(Q(name__icontains=i),q.OR)

    product=Product.objects.filter(q)
    product=list(product.values())
    product=list((p['id'],p['name'],p['brand']) for p in product)
    print(product)
    # for i in product:
    #     print(i)
    cur1 = list(Product.objects.all().values_list('id', flat=True))
    cur2=list(Product.objects.all().values_list('name', flat=True))
    cur3 = list(Product.objects.all().values_list('brand', flat=True))

    cur = zip(cur1,cur2,cur3)

    # print(te[0])
    cur = sorted(list(cur),key=lambda x : len(x[1]))
    cur2 = sorted(list(Product.objects.all().values_list('name', flat=True)), key=len)
    # for i, data in enumerate(cur):
    #     data=data[1]
    #     data2=cur2[i]
    #     assert data==data2, "같지않네요"
    #
    # # print(cur)
    #
    lenDict=getChunk(cur2)
    # print(lenDict)
    # print(lenDict[str(1)])
    # print(cur[23])
    # # print(cur[153159])
    # # print(lenDict)
    target="쓰리씨이 아이 스위치"
    # print(len(target))
    # target = "레드 블레미쉬 클리어 수딩 크림"
    t1=time.time()
    result1=compData_chunk(cur,lenDict,target,score=90)
    t1=time.time()-t1
    print(t1, result1[len(result1)-1])
    # print(result1)
    t2=time.time()
    result2=compData_full(cur,target)
    t2=time.time()-t2
    print(t2, result2[len(result2)-1])
    # for i in result1:
    #     print(i)
    # for i in result2:
    #     print(i)
    # experiments(cur,lenDict,score=95)
    # # print(result1)
    # # print(result2)
    #
    #
    #