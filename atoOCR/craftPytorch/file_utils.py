# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2


# borrowed from https://github.com/lengstrom/fast-style-transfer/blob/master/src/utils.py
def get_files(img_dir):
    imgs, masks, xmls = list_files(img_dir)
    return imgs, masks, xmls

def list_files(in_path):
    img_files = []
    mask_files = []
    gt_files = []
    for (dirpath, dirnames, filenames) in os.walk(in_path):
        for file in filenames:
            filename, ext = os.path.splitext(file)
            ext = str.lower(ext)
            if ext == '.jpg' or ext == '.jpeg' or ext == '.gif' or ext == '.png' or ext == '.pgm':
                img_files.append(os.path.join(dirpath, file))
            elif ext == '.bmp':
                mask_files.append(os.path.join(dirpath, file))
            elif ext == '.xml' or ext == '.gt' or ext == '.txt':
                gt_files.append(os.path.join(dirpath, file))
            elif ext == '.zip':
                continue
    # img_files.sort()
    # mask_files.sort()
    # gt_files.sort()
    return img_files, mask_files, gt_files

def saveResult(img_file, img, boxes, dirname='./result/', verticals=None, texts=None):
        """ save text detection result one by one
        Args:
            img_file (str): image file name
            img (array): raw image context
            boxes (array): array of result file
                Shape: [num_detections, 4] for BB output / [num_detections, 4] for QUAD output
        Return:
            None
        """
        img = np.array(img)

        # make result file list
        filename, file_ext = os.path.splitext(os.path.basename(img_file))

        # result directory
        res_file = dirname + "res_" + filename + '.txt'
        res_img_file = dirname + "res_" + filename + '.jpg'

        if not os.path.isdir(dirname):
            os.mkdir(dirname)

        with open(res_file, 'w') as f:
            for i, box in enumerate(boxes):
                poly = np.array(box).astype(np.int32).reshape((-1))
                strResult = ','.join([str(p) for p in poly]) + '\r\n'
                f.write(strResult)

                poly = poly.reshape(-1, 2)
                # print(poly)
                # print(poly.reshape((-1, 1, 2)))
                # print(len(poly.reshape((-1, 1, 2))))
                arr=poly.reshape((-1, 1, 2))
                # print(arr[0][0])
                # print(arr[0][0][0],arr[2][0][0],arr[0][0][1],arr[2][0][1])

                croped=img[arr[0][0][1]:arr[2][0][1],arr[0][0][0]:arr[2][0][0]]
                # cv2.imshow("cr",croped)
                # cv2.waitKey(0)
                cv2.polylines(img, [poly.reshape((-1, 1, 2))], True, color=(0, 0, 255), thickness=2)
                ptColor = (0, 255, 255)
                if verticals is not None:
                    if verticals[i]:
                        ptColor = (255, 0, 0)

                if texts is not None:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.5
                    cv2.putText(img, "{}".format(texts[i]), (poly[0][0]+1, poly[0][1]+1), font, font_scale, (0, 0, 0), thickness=1)
                    cv2.putText(img, "{}".format(texts[i]), tuple(poly[0]), font, font_scale, (0, 255, 255), thickness=1)

        # Save result image
        cv2.imwrite(res_img_file, img)


def saveResult_modified(img_file, img, boxes, dirname='./result/', verticals=None, texts=None):
    """ save text detection result one by one
    Args:
        img_file (str): image file name
        img (array): raw image context
        boxes (array): array of result file
            Shape: [num_detections, 4] for BB output / [num_detections, 4] for QUAD output
    Return:
        None
    """
    img = np.array(img)
    img = np.ascontiguousarray(img, dtype=np.uint8)
    src = np.array(img)
    # make result file list
    filename, file_ext = os.path.splitext(os.path.basename(img_file))

    # result directory
    res_file = dirname + "res_" + filename + '.txt'


    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    imgs=[]
    points=[]
    with open(res_file, 'w') as f:
        for i, box in enumerate(boxes):
            poly = np.array(box).astype(np.int32).reshape((-1))
            strResult = ','.join([str(p) for p in poly]) + '\r\n'
            f.write(strResult)

            poly = poly.reshape(-1, 2)
            # print(poly)
            # print(poly.reshape((-1, 1, 2)))
            # print(len(poly.reshape((-1, 1, 2))))
            arr = poly.reshape((-1, 1, 2))
            # print(arr[0][0][1])
            # print(arr)
            ltx, lty = arr[0][0]
            rtx, rty = arr[1][0]
            rbx, rby = arr[2][0]
            lbx, lby = arr[3][0]
            x1 = ltx
            y1 = min(lty, rty)
            x2 = rbx
            y2 = max(rby, lby)

            # print(arr[0][0])
            # print(arr[0][0][0], arr[2][0][0], arr[0][0][1], arr[2][0][1])
            # croped = src[arr[0][0][1]:arr[2][0][1], arr[0][0][0]:arr[2][0][0]]
            croped = src[y1:y2, x1:x2]
            # y1,y2=(arr[0][0][1],arr[2][0][1])
            # x1,x2=(arr[0][0][0]<arr[2][0][0])
            # points.append((arr[0][0][1],arr[0][0][0]))


            # print(ltx,lty,rtx,rty,rbx,rby,lbx,lby)
            # points.append((arr[0][0][1], arr[0][0][0],arr[2][0][1],arr[2][0][0]))
            points.append((y1, x1, y2, x2))
            #print((y1, x1, y2, x2))
            #print(poly.reshape((-1, 1, 2)))
            # for i in poly.reshape((-1, 1, 2)):
            #     i=i[0]
            #     row,col=i
            #     cv2.circle(img,i,5,(255,255,255))
            # cv2.imshow("img",img)
            # cv2.waitKey(0)

            cv2.polylines(img, [poly.reshape((-1, 1, 2))], True, color=(0, 0, 255), thickness=2)
            ptColor = (0, 255, 255)
            if verticals is not None:
                if verticals[i]:
                    ptColor = (255, 0, 0)

            if texts is not None:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                cv2.putText(img, "{}".format(texts[i]), (poly[0][0] + 1, poly[0][1] + 1), font, font_scale, (0, 0, 0),
                            thickness=10)
                cv2.putText(img, "{}".format(texts[i]), tuple(poly[0]), font, font_scale, (0, 255, 255), thickness=1)

            imgs.append(croped)


    # Save result image
    return imgs,img,points