from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
import os

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cdm = "C:/Program Files/Tesseract-OCR/tesseract.exe"

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
            resulttext = pytesseract.image_to_string(imgfile, lang='kor')

    context['imgname'] = imgname
    context['resulttext'] = resulttext.replace(" ","")
    return render(request, 'coocr_upload.html', context)


