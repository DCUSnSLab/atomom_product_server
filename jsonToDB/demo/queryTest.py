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
difflib.SequenceMatcher = CSequenceMatcher

# https://runebook.dev/ko/docs/django/topics/db/sql
# https://stackoverflow.com/questions/17903706/how-to-sort-list-of-strings-by-best-match-difflib-ratio
# https://stackoverflow.com/questions/25680947/pythons-difflib-sequencematcher-speed-up
if __name__ == '__main__':
    # print("% %")
    # query="select * from atomom_product where name like \' %%에이지%%\';"
    # print(query)
    # queryset=Product.objects.raw(query)
    # print(type(queryset))
    #
    # for i, data in enumerate(queryset):
    #     print(i)
    #     print(data)
    #     print(data.name)

    # text="르 몬스터"
    # cur = Product.objects.filter(name__contains=text)
    # id= "ddddd"
    # text="dddddd"
    # Product.object.
    # for data in cur:
    #     # print(data.id,data.korean)
    #     print(data.name)
    #         # break
    inputText = "닥터지 레드 블레미쉬 클리어 수딩 크림 moistunz"
    outputText= None
    cur = list(Product.objects.all().values_list('name', flat=True))
    cur=sorted(cur, key=lambda x: difflib.SequenceMatcher(None, x, inputText).ratio(), reverse=True)
    print(cur[0:10])
    # maxRatio=0
    # for data in cur:
    #     # print(data.id,data.korean)
    #
    #     ratio = difflib.SequenceMatcher(None, inputText, data.name).ratio()
    #     temp=maxRatio
    #
    #     maxRatio=max(maxRatio,ratio)

        # break





    # print(numberToBase(1000, 16))

