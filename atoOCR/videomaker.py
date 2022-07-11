import cv2
import numpy as np
import copy


def subReduceValue(img,value):
    array = np.full(img.shape, (value, value, value), dtype=np.uint8)
    sub_dst = cv2.subtract(img, array)
    return sub_dst


def reduceValue(img,pos):
    h,w,_=img.shape
    startY, endY, startX, endX=pos
    value=100
    img[0:startY, 0:w] = subReduceValue(img[0:startY, 0:w],value)  # 위
    img[endY:h, 0:w] = subReduceValue(img[endY:h, 0:w],value)  # 아래
    img[startY:endY, 0:startX] = subReduceValue(img[startY:endY, 0:startX],value)  # 왼
    img[startY:endY, endX:w] = subReduceValue(img[startY:endY, endX:w],value)  # 오른


    return img
    pass

def setRoi(img,cap):
    ratio=( () )
    h,w,_=img.shape
    dstH=h
    dstW=w
    while (dstH > int(h / 2)):
        dstH -= 9
    while (dstW > int(w / 2)):
        dstW -= 16
    cH=int(h/2)
    cW=int(w/2)
    startY=int(cH/2)
    endY=int(cH/2)+dstH
    startX=int(cW/2)
    endX=int(cW/2)+dstW
    # print(startY,endY,startX,endX)
    # print(dstH,dstW)
    cropped=copy.deepcopy(img[startY:endY,startX:endX])
    pos=(startY,endY,startX,endX)
    pos=(startY,endY,startX,endX)
    img=reduceValue(img,pos)
    img=cv2.rectangle(img,(startX,startY),(endX,endY),(255,0,0),3)
    #cv2.imshow("cropped",cropped )
    # print(cropped.shape)
    return img,cropped,pos

    pass

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)


    w=1920
    h=1080
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('save.avi', fourcc, 25.0, (w, h))
    print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

    while(True):
        ret, frame = cap.read()    # Read 결과와 frame
        frame,cropped,pos=setRoi(frame,cap)
        frame[pos[0]:pos[1],pos[2]:pos[3]]=0
        if(ret) :
            gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
            # cv2.namedWindow('frame_color',cv2.WINDOW_NORMAL)
            cv2.imshow('frame_color', frame)    # 컬러 화면 출력        cv2.imshow('frame_gray', gray)    # Gray 화면 출력
            out.write(frame)

            if cv2.waitKey(1) == ord('q'):
                cap.release()
                break
    cv2.destroyAllWindows()