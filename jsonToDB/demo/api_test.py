import os.path

import cv2
import requests
import json
# https://runebook.dev/ko/docs/django/ref/request-response
fileName='104.jpg'
origin_path="../../cosmetic_demo_image"
roi_path="../../test_image"
img=cv2.imread(os.path.join(origin_path,fileName))
rows,cols,_=img.shape
data={'rows': str(rows), 'cols': str(cols)}
files = {'media': open(os.path.join(roi_path,fileName), 'rb')}
print(type(files))

# response=requests.post("http://203.250.32.251:8000/coocr_upload",files=files)
response=requests.post("http://203.250.32.251:8000/api",files=files,cookies=data)
j=response.json()
path='C:/Users/dgdgk/Documents'
file_name=fileName.split(".")
print(fileName,file_name)
file_name=file_name[0]+".json"
with open(os.path.join(path,file_name), 'w',encoding='UTF-8') as outfile:
    json.dump(j, outfile,ensure_ascii=False)
# print(response.json())
# print(response.content)
# print(response.text)
# print(response.content)