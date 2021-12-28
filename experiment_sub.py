import cv2
import os

if __name__ == '__main__':
    basePath = '../test/4032x3024/'
    savePath='../test/640x480/'
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    fileList = os.listdir(basePath)
    resolution=(640,480)

    for i in range(len(fileList)):
        imgPath = basePath + fileList[i]
        #rint(base/Path+"간판_가로형간판_123413.jpg")
        print(imgPath)
        img=cv2.imread(imgPath)
        img2=cv2.resize(img,dsize=resolution,interpolation=cv2.INTER_AREA)

        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.namedWindow("img2", cv2.WINDOW_NORMAL)
        cv2.imshow("img", img)
        cv2.imshow("img2", img)
        cv2.waitKey(1)
        cv2.imwrite(savePath+fileList[i],img2)
    pass