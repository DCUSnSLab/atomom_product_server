from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os, sys

from PIL import Image
import cv2
curPath=os.getcwd()
path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
print(path)
# print(os.listdir(path))
path=os.path.join(path,'atoOCR')
print(path)
sys.path.append(path)
import demo_modifed_for_one_image_processing as ocr
os.chdir(path)
craftModel, model, opt = ocr.setModel()
os.chdir(curPath)
def home(request):
    context = {}
    context['menutitle'] = 'HOME'

    return render(request, 'home.html', context)

def groupby(points,texts,img):
    rows,cols,_ =img.shape
    rThres = int(rows / 100)
    cThres = int(cols / 20)
    # newPoint

    datas=[]
    #포인트들에 텍스트 추가 (1,3,2,3,타이레놀)
    for i, point in enumerate(points):
        # print(i,point,texts[i])
        r1, c1, r2, c2 = point
        data=(r1,c1,r2,c2,texts[i])
        datas.append(data)

    check=False
    br=0
    splitIndex=[]
    for i, data in enumerate(datas):
        r1, c1,r2,c2,t = data
        if(check==False):
            br=r1
            check=True
            continue
        if(rThres<int(r1-br)):
            splitIndex.append(i)
        else:
            pass
        br=r1
    newTexts=""

    b=0
    newDatas=[]
    for i in range(len(splitIndex)):
        rowi=i
        i=splitIndex[i]
        data=datas[b:i]

        data = sorted(data, key=lambda x: (x[1]))
        b=i
        for i in data:
            newDatas.append(i)
        if(rowi==len(splitIndex)-1):
            # print(len(datas),i)
            data = datas[b:len(datas)]
            # print(data)
            # print(data)
            data = sorted(data, key=lambda x: (x[1]))
            for i in data:
                newDatas.append(i)
    print("-"*50)
    print(newDatas)
    newTexts=""
    check=False
    bdata=0
    # print(img.shape)
    centroid=0
    bcentroid=0
    rThres = int(rows / 30)
    for i, data in enumerate(newDatas):
        if(check==False):
            check=True
            bdata=data
            br1, bc1, br2, bc2, t = bdata
            newTexts+=t
            continue
        br1, bc1, br2, bc2, t = bdata
        r1, c1, r2, c2, t = data
        bcentroid=abs(br2-br1)+br1
        centroid=abs(r2-r1)+r1
        print(bdata, data)
        print("     bcentroid,centroid, rThres, int(abs(bcentroid-centroid))",bcentroid,centroid,rThres,int(abs(bcentroid-centroid)))
        if(rThres>int(abs(bcentroid-centroid))):

            print("     ",cThres,abs(int(c1-bc2)))
            if(cThres>abs(int(c1-bc2))):
                newTexts+=' '
            else:
                newTexts += '\n'
        else:
            newTexts+='\n'
        newTexts+=t
        bdata=data
    print(newTexts)
    return newTexts


    #
    # for i, data in enumerate(newDatas):
    #     r1, c1, r2, c2, t = data
    #     newTexts+=t
    #     if i in splitIndex:
    #         newTexts+='\n'
    # print("-" * 50)
    # print(newTexts)
    # print("-" * 50)




def coocr_upload(request):
    context = {}
    context['menutitle'] = 'OCR READ'

    imgname = ''
    resulttext = ''
    parsedText=''
    resultImgname=""
    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile', '')

        if uploadfile != '':
            name_old = uploadfile.name
            name_ext = os.path.splitext(name_old)[1]

            fs = FileSystemStorage(location='static/source')
            imgname = fs.save(f"src-{name_old}", uploadfile)
            # print(uploadfile)
            # print(type(uploadfile))
            # print(imgname)


            imgfile = Image.open(f"./static/source/{imgname}")
            imgPath=curPath+f"./static/source/{imgname}"

            os.chdir(path)
            img, points = ocr.craftOperation(imgPath, craftModel, dirPath=opt.image_folder)
            texts = ocr.demo(opt,model)
            # print(points)
            # print(texts)
            parsedText=groupby(points,texts,img)
            # img = ocr.putText(img, points, texts)
            ocr.mkdir()

            resulttext = texts
            os.chdir(curPath)
            # print(f"{imgname}")
            # print(imgname)
            name, ext = os.path.splitext(imgname)
            # print('name :', name)
            # print('ext :', ext)
            resultImgname=name+"_result"+ext

            cv2.imwrite(curPath+f"./static/source/{resultImgname}",img)


    context['imgname'] = imgname
    context['resultImgname'] = resultImgname
    resulttext='\n'.join(resulttext)
    print(type(resulttext))
    # context['resulttext'] = '\n'+resulttext
    context['resulttext'] = '\n' + parsedText
    return render(request, 'coocr_upload.html', context)
