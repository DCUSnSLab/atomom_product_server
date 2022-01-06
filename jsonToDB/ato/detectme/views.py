from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading

# https://blog.miguelgrinberg.com/post/video-streaming-with-flask/page/8

def home(request):
    context = {}

    return render(request, "home.html")

class VideoCamera(object):
    def __init__(self):
        import os, sys
        path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
        print(path)
        # print(os.listdir(path))
        path=os.path.join(path,'atoOCR')
        print(path)
        sys.path.append(path)
        import demo_modifed_for_one_image_processing as ocr
        craftModel, model, opt = ocr.setModel()



        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        import sys
        # sys.path.append("..")
        # import asdfg
        import os



        image = self.frame
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
