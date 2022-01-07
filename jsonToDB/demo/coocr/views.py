from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os, sys

from PIL import Image
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


def coocr_upload(request):
    context = {}
    context['menutitle'] = 'OCR READ'

    imgname = ''
    resulttext = ''
    if 'uploadfile' in request.FILES:
        uploadfile = request.FILES.get('uploadfile', '')

        if uploadfile != '':
            name_old = uploadfile.name
            name_ext = os.path.splitext(name_old)[1]

            fs = FileSystemStorage(location='static/source')
            imgname = fs.save(f"src-{name_old}", uploadfile)


            imgfile = Image.open(f"./static/source/{imgname}")
            imgPath=curPath+f"./static/source/{imgname}"

            os.chdir(path)
            img, points = ocr.craftOperation(imgPath, craftModel, dirPath=opt.image_folder)
            texts = ocr.demo(opt,model)
            img = ocr.putText(img, points, texts)
            image = img
            ocr.mkdir()

            resulttext = texts
            os.chdir(curPath)


    context['imgname'] = imgname
    context['resulttext'] = resulttext
    return render(request, 'coocr_upload.html', context)


