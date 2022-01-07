from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import os, sys
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8

def home(request):
    context = {}

    return render(request, "home.html")

class VideoCamera(object):
    def __init__(self):

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
        self.craftModel=craftModel
        self.model=model
        self.opt=opt
        self.ocrPath=path
        self.djangoPath=curPath
        os.chdir(curPath)



        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        imgPath = self.ocrPath+"/curImage.jpg"
        print('-'*50)
        print(imgPath)
        print('-' * 50)
        cv2.imwrite(imgPath,image)

        import demo_modifed_for_one_image_processing as ocr

        os.chdir(self.ocrPath)
        img, points = ocr.craftOperation(imgPath, self.craftModel, dirPath=self.opt.image_folder)
        texts = ocr.demo(self.opt, self.model)
        img = ocr.putText(img, points, texts)
        image=img
        os.chdir(self.djangoPath)




        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass
