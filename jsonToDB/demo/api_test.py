import os.path
import argparse
import cv2
import requests
import json
from tqdm import tqdm
# https://runebook.dev/ko/docs/django/ref/request-response
def getSingle(opt):
    fileName=opt.fileName
    origin_path="../../cosmetic_demo_image"
    roi_path="../../test_image"
    img=cv2.imread(os.path.join(origin_path,fileName))
    rows,cols,_=img.shape
    data={'rows': str(rows), 'cols': str(cols)}
    files = {'media': open(os.path.join(roi_path,fileName), 'rb')}
    print(type(files))

    # response=requests.post("http://203.250.32.251:8000/coocr_upload",files=files)
    # response = requests.post("http://203.250.32.251:8000/api", files=files, cookies=data, params=data)
    response = requests.post("http://203.250.32.251:8000/api", files=files,  params=data)
    j=response.json()
    path='C:/Users/dgdgk/Documents'
    file_name=fileName.split(".")
    print(fileName,file_name)
    file_name=file_name[0]+".json"
    with open(os.path.join(path,file_name), 'w',encoding='UTF-8') as outfile:
        # json.dump(j, outfile,ensure_ascii=False,indent='\t')
        json.dump(j, outfile, ensure_ascii=False, indent='\t')
    # print(response.json())
    # print(response.content)
    # print(response.text)
    # print(response.content)
def getMulti(opt):
    fileName=opt.fileName
    origin_path=opt.origin_path
    roi_path=opt.roi_path
    fileEx = r'.jpg'
    origin_list = [file for file in os.listdir(origin_path) if file.endswith(fileEx)]
    roi_list = [file for file in os.listdir(roi_path) if file.endswith(fileEx)]
    # assert len(origin_list)==len(roi_list), "len(origin_list) : "+str(len(origin_list))+" len(roi_list) : "+str(len(roi_list))

    for i in tqdm(range(len(roi_list))):
        fileName=roi_list[i]
        img=cv2.imread(os.path.join(origin_path,fileName))
        rows,cols,_=img.shape
        data={'rows': str(rows), 'cols': str(cols)}
        files = {'media': open(os.path.join(roi_path,fileName), 'rb')}
        # print(type(files))

        # response=requests.post("http://203.250.32.251:8000/coocr_upload",files=files)
        response=requests.post("http://203.250.32.251:8000/api",files=files,cookies=data)
        j=response.json()
        path='C:/Users/dgdgk/Documents'
        file_name=fileName.split(".")
        # print(fileName,file_name)
        file_name=file_name[0]+".json"
        with open(os.path.join(path,file_name), 'w',encoding='UTF-8') as outfile:
            json.dump(j, outfile, ensure_ascii=False, indent='\t')
        # print(response.json())
        # print(response.content)
        # print(response.text)
        # print(response.content)



if __name__ == '__main__':
    # python ./api_test.py --single True --fileName 003.jpg
    # python ./api_test.py --multi True
    parser = argparse.ArgumentParser()
    parser.add_argument('--fileName')
    parser.add_argument('--origin_path', default="../../cosmetic_demo_image")
    parser.add_argument('--roi_path', default="../../test_image")
    parser.add_argument('--single', default=False,help="True or False")
    parser.add_argument('--multi', default=False,help="True or False")
    opt=parser.parse_args()
    # print((opt.single == "Treu"))
    assert opt.single == "True" or opt.multi == "True", "single or mulit 둘 중 하나는 true여야합니다"
    if(opt.single=="True"):
        assert opt.fileName != None, "fileName을 입력해주세요"
        getSingle(opt)
    else:
        assert opt.fileName == None, "fileName을 입력하지마세요"
        getMulti(opt)




# import os.path
#
# import cv2
# import requests
# import json
#
#
# if __name__ == '__main__':
#
#     # https://runebook.dev/ko/docs/django/ref/request-response
#     fileName='023.jpg'
#     origin_path="../../cosmetic_demo_image"
#     roi_path="../../test_image"
#     img=cv2.imread(os.path.join(origin_path,fileName))
#     rows,cols,_=img.shape
#     data={'rows': str(rows), 'cols': str(cols)}
#     files = {'media': open(os.path.join(roi_path,fileName), 'rb')}
#     print(type(files))
#
#     # response=requests.post("http://203.250.32.251:8000/coocr_upload",files=files)
#     response=requests.post("http://203.250.32.251:8000/api",files=files,cookies=data)
#     j=response.json()
#     path='C:/Users/dgdgk/Documents'
#     file_name=fileName.split(".")
#     print(fileName,file_name)
#     file_name=file_name[0]+".json"
#     with open(os.path.join(path,file_name), 'w',encoding='UTF-8') as outfile:
#         json.dump(j, outfile,ensure_ascii=False)
#     # print(response.json())
#     # print(response.content)
#     # print(response.text)
#     # print(response.content)