# -*- coding: utf-8 -*-
"""
Copyright (c) 2019-present NAVER Corp.
MIT License
"""


import sys
import os

import time
import argparse

import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from PIL import Image

import cv2
from skimage import io
import numpy as np
from craftPytorch import craft_utils
from craftPytorch import imgproc
from craftPytorch import file_utils
import json
import zipfile

# from craft import CRAFT
from craftPytorch import craft_modified
from collections import OrderedDict
import shutil
def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict

def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")
#
# parser = argparse.ArgumentParser(description='CRAFT Text Detection')
# parser.add_argument('--trained_model', default='weights/craft_mlt_25k.pth', type=str, help='pretrained model')
# parser.add_argument('--text_threshold', default=0.7, type=float, help='text confidence threshold')
# parser.add_argument('--low_text', default=0.4, type=float, help='text low-bound score')
# parser.add_argument('--link_threshold', default=0.4, type=float, help='link confidence threshold')
# parser.add_argument('--cuda', default=True, type=str2bool, help='Use cuda for inference')
# parser.add_argument('--canvas_size', default=1280, type=int, help='image size for inference')
# parser.add_argument('--mag_ratio', default=1.5, type=float, help='image magnification ratio')
# parser.add_argument('--poly', default=False, action='store_true', help='enable polygon type')
# parser.add_argument('--show_time', default=False, action='store_true', help='show processing time')
# parser.add_argument('--test_folder', default='/data/', type=str, help='folder path to input images')
# parser.add_argument('--refine', default=False, action='store_true', help='enable link refiner')
# parser.add_argument('--refiner_model', default='weights/craft_refiner_CTW1500.pth', type=str, help='pretrained refiner model')
#
# args = parser.parse_args()


""" For test images in a folder """


def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly,args, refine_net=None):
    t0 = time.time()
    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image, args.canvas_size, interpolation=cv2.INTER_LINEAR, mag_ratio=args.mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio
    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)    # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))                # [c, h, w] to [b, c, h, w]
    
    # print(cuda)
    if cuda:
        x = x.cuda()
    t0 = time.time() - t0
    # forward pass
    t1 = time.time()
    with torch.no_grad():
        y, feature = net(x)
    t1 = time.time() - t1
    # make score and link map
    t2 = time.time()
    score_text = y[0,:,:,0].cpu().data.numpy()
    score_link = y[0,:,:,1].cpu().data.numpy()
    t2 = time.time() - t2
    # refine link
    t3 = time.time()
    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0,:,:,0].cpu().data.numpy()
    t3 = time.time() - t3
    t4 = time.time()
    # Post-processing

    boxes, polys = craft_utils.getDetBoxes(score_text, score_link, text_threshold, link_threshold, low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None: polys[k] = boxes[k]

    t4 = time.time() - t4
    # render results (optional)
    t5 = time.time()
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)
    t5 = time.time() - t5

#     print("t1",t1)
    # print("t2", t2)
    # print("t3", t3)
    # print("t4", t4)
    # print("t5", t5)
    if args.show_time : print("\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

    return boxes, polys, ret_score_text
def loadModel():
    t0=time.time()
    args = argparse.Namespace(
        trained_model=str("./craftPytorch/craft_mlt_25k.pth"),
        text_threshold=float(0.7),
        low_text=float(0.4),
        link_threshold=float(0.4),
        cuda=str2bool("True"),
        canvas_size=int(1280),
        mag_ratio=float(1),
        poly=False,
        show_time=False,
        test_folder=str("./test/"),
        refine=False,
        refiner_model=str('weights/craft_refiner_CTW1500.pth')
    )
    
    if not (os.path.isdir(args.test_folder)):
        os.makedirs(os.path.join(args.test_folder))

    image_list, _, _ = file_utils.get_files(args.test_folder)
    # print("이거 타입은", type(image_list))
    # print(image_list)
    result_folder = './result/'
    if not os.path.isdir(result_folder):
        os.mkdir(result_folder)
    t0=time.time()-t0
    #
    # print("-------------------")

    #
    # print(args)
    # print("-------------------")
    # image_list.append(imgPath)
    # load net
    t1=time.time()
    net = craft_modified.CRAFT(pretrained=True).cuda()  # initialize
    t1=time.time()-t1
    # print('Loading weights from checkpoint (' + args.trained_model + ')')
    t2=time.time()
    if args.cuda:
        net.load_state_dict(copyStateDict(torch.load(args.trained_model)))
    else:
        net.load_state_dict(copyStateDict(torch.load(args.trained_model, map_location='cpu')))
    t2=time.time()-t2
    t3=time.time()
    if args.cuda:
        net = net.cuda()
        net = torch.nn.DataParallel(net)
        cudnn.benchmark = False

    net.eval()

    # LinkRefiner
    refine_net = None
    t3=time.time()-t3
#     print("load_model t0",t0)
#     print("load_model t1",t1)
#     print("load_model t2",t2)
#     print("load_model t3",t3)

    return (net,args,refine_net,result_folder)
def main(imgPath,model):
    
    image_list=[imgPath]
    net,args,refine_net,result_folder=model
    t = time.time()

    # load data
    time2=time.time()
    cnt=0
    for k, image_path in enumerate(image_list):
        # print("cnt",cnt)
        cnt+=1
        time3=time.time()
        image = imgproc.loadImage(image_path)
        time3=time.time()-time3
        time4=time.time()
        bboxes, polys, score_text = test_net(net, image, args.text_threshold, args.link_threshold, args.low_text,
                                             args.cuda, args.poly,args, refine_net)
        time4=time.time()-time4
        # print(type(bboxes),type(polys))

        # save score text
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = result_folder + "/res_" + filename + '_mask.jpg'
        # cv2.imshow("1",bboxes)
        # cv2.waitKey(0)
        # cv2.imwrite(mask_file, score_text) # 파란거
        time5=time.time()
        imgs,img,points=file_utils.saveResult_modified(image_path, image[:, :, ::-1], polys, dirname=result_folder)
        time5=time.time()-time5

#     print("추론 및 저장 시간",time.time()-time2)
#     print("    이미지 로드",time3)
#     print("     추론 시간",time4)
#     print("     저장 시간",time5)

    # print("elapsed time : {}s".format(time.time() - t))
    # shutil.rmtree(args.test_folder)

    if os.path.exists(args.test_folder):
        for file in os.scandir(args.test_folder):
            os.remove(file.path)
    

    return imgs,img,points

if __name__ == '__main__':
    imgPath="./test/name2.png"
    imgPath = "./test/name10_out.png"
    imgs=main(imgPath)
    for i in imgs:
        # i=cv2.Canny(i,0,255)
        cv2.imshow("d",i)
        print(getText(i))
        cv2.waitKey(0)

