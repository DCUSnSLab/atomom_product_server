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
from atomom.models import Product
from atomom.models import SubProduct
from cdifflib import CSequenceMatcher
import difflib
import numpy as np


# https://runebook.dev/ko/docs/django/topics/db/sql
# https://stackoverflow.com/questions/17903706/how-to-sort-list-of-strings-by-best-match-difflib-ratio
# https://stackoverflow.com/questions/25680947/pythons-difflib-sequencematcher-speed-up

# python -m cProfile -o prof.prof queryTest.py
# snakeviz prof.prof

import matplotlib.pyplot as plt
from jaro import get_jaro_distance
def operation():
    difflib.SequenceMatcher = CSequenceMatcher
    inputText = "닥터지 레드 블레마쉬 클라어 수분 크림 Mos"
    outputText = None
    sortTime=time.time()
    cur = sorted(list(Product.objects.all().values_list('name', flat=True)),key=len)
    # for i, data in enumerate(cur):
    #     print(i,data,len(data))
    print(time.time()-sortTime)
    # cur.split(len())

    os.system('pause')
    # cur = list(Product.objects.all().values_list('name', flat=True))
    # print(type(cur))
    t1=time.time()
    # sd=difflib.SequenceMatcher(None,cur,inputText).quick_ratio()

    seq = difflib.SequenceMatcher()
    seq.set_seq1(inputText)
    maxValue=0
    result_list=[]
    xL=[]
    yL=[]
    # func=
    t1=time.time()
    for i, data in enumerate(cur):


        # print(cur_ratio)
        seq.set_seq2(data)

        # cur_ratio=seq.quick_ratio()*100

        # cur_ratio = get_jaro_distance(inputText,data, winkler=True, scaling=0.1) * 100
        # if(data=="레드 블레미쉬 클리어 수딩 크림"):
        #     print(cur_ratio)
        cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
        if(maxValue<=cur_ratio):
            result_list.append((i,data,cur_ratio))
            maxValue=cur_ratio
        if(cur_ratio>90):
            break
    print(result_list)
    print(time.time()-t1)
    #     xL.append(i)
    #     yL.append(cur_ratio)
    # plt.scatter(xL,yL)
    # plt.xlabel('X-Label')
    # plt.ylabel('Y-Label')
    # plt.show()
        # os.system('pause')
    # for i in result_list:
    #     print(i)

    # key=lambda x: difflib.SequenceMatcher(None, x, inputText).quick_ratio()
    # # print(time.time()-t1)
    # # print(key)
    # cur = sorted(cur, key=key, reverse=True)
    # print(max(cur, key=lambda x: difflib.SequenceMatcher(None, x, inputText).ratio()))

def skipCheck(skip):
    pass

def operation2(lis):
    difflib.SequenceMatcher = CSequenceMatcher

    cur = np.array(sorted(list(Product.objects.all().values_list('name', flat=True))))

    seq = difflib.SequenceMatcher()
    xL = []
    yL = []
    cnt=0
    skipMinDistance=-1
    for inputText in tqdm(range(len(lis))):

        inputText=lis[inputText]
        inputText=inputText[0]
        # os.system('pause')
        seq.set_seq1(inputText)
        maxValue=0
        result_list=[]
        xL = []
        yL = []

        before=0
        for i, data in enumerate(cur):
            # print(cur_ratio)
            seq.set_seq2(data)

            # print(inputText,data)
            # print("     ",seq.ratio()*100)
            cur_ratio=seq.quick_ratio()*100

            # cur_ratio = (lambda x: seq.quick_ratio() * 100)(0)
            if(maxValue<=cur_ratio):

                # print(inputText, '\033[31m', data, '\033[0m', cur_ratio)
                result_list.append((i,data,cur_ratio))
                maxValue=cur_ratio
            # if(cur_ratio>60):
            #     xL.append(i)
            #     yL.append(cur_ratio)

            xL.append(i)
            yL.append(cur_ratio)
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams["figure.figsize"] = (6, 6)
        plt.rcParams['axes.unicode_minus'] = False
        plt.scatter(xL,yL,s=0.4)
        # print(result_list[len(result_list)-1])
        plt.xlabel(inputText+"  \n  "+str(result_list[len(result_list)-1]))
        plt.ylabel('similarity_ratio')
        plt.xlim([0, 153176])
        plt.ylim([0, 100])
        # plt.show()
        path='./experiment/result/'
        if not os.path.exists(path):
            os.makedirs(path)
        plt.savefig(path+str(cnt)+'.png')
        plt.cla()
        cnt+=1
        # os.system('pause')


# https://blog.paperspace.com/implementing-levenshtein-distance-word-autocomplete-autocorrect/
def exp(cnt):
    fr = open('./experiment/experiment_'+str(cnt) + '.csv', 'r', newline='', encoding='UTF-8-sig')
    rdr = csv.reader(fr)
    lis=list(rdr)
    operation2(lis)

from numba import jit

@jit(nopython=True)
def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

@jit(nopython=True)
def get_levenshtein(tests, target,result):
    # np.array(dtype=)
    for i, data in enumerate(tests):
        re=levenshtein(data, target)
        # result=np.append(result,levenshtein(data, target))


    # return levenshtein(s1,s2)

if __name__ == '__main__':
    operation()
    # texts = np.array(list(Product.objects.all().values_list('name', flat=True)))
    # target="1025 독도 토너"
    # t1=time.time()
    # result=np.array(["em"])
    # print(get_levenshtein(texts,target,result))
    # print(result)
    # print(time.time()-t1)
    # exp(0)
    # exp(1)
    # exp(2)
    # from queryTest_save import operation as o
    # o()

    # distance = levenshteinDistanceDP("1025 독도 토너", "독도 토너")
    # texts=['1025','독','독도','독도토너','1025 독도 토너',
    #        '1023 독도','안녕','하','세','요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요',
    #        '1025', '독', '독도', '독도토너', '1025 독도 토너',
    #        '1023 독도', '안녕', '하', '세', '요'
    #        ]
    # texts=np.array(list(Product.objects.all().values_list('name', flat=True)))
    # # t1=time.time()
    # test(texts,"1025 독도 토너")
    # print(time.time()-t1)
    # # distance = levenshteinDistanceDP("abcde", "abc")
    # # print(distance)
    pass
