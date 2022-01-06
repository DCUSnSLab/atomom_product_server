""" a modified version of CRNN torch repository https://github.com/bgshih/crnn/blob/master/tool/create_dataset.py """

import fire
import os
import lmdb
import cv2
from tqdm import tqdm
import numpy as np


def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    imageBuf = np.frombuffer(imageBin, dtype=np.uint8)
    img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
    imgH, imgW = img.shape[0], img.shape[1]
    if imgH * imgW == 0:
        return False
    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k, v)


def createDataset(inputPath, gtFile, outputPath, checkValid=True):
    """
    Create LMDB dataset for training and evaluation.
    ARGS:
        inputPath  : input folder path where starts imagePath
        outputPath : LMDB output path
        gtFile     : list of image path and label
        checkValid : if true, check the validity of every image
    """
    os.makedirs(outputPath, exist_ok=True)
    # env = lmdb.open(outputPath, map_size=1099511627776/1024) #lmdb.MapFullError: mdb_put: MDB_MAP_FULL: Environment mapsize limit reached
    # env = lmdb.open(outputPath, map_size=1099511627776 / 1024*10)
    # env = lmdb.open(outputPath, map_size=1099511627776 / 1024 * 1) # 4만까지 밖에 안됨
    # env = lmdb.open(outputPath, map_size=1099511627776 / 1024 * 2.2) # train
    env = lmdb.open(outputPath, map_size=1099511627776 / 1024 * 15)
    cache = {}
    cnt = 1

    #아래와 같이 인코딩시에는 한글이 꺠져서 학습이 안되어요 이러지마세요
    # with open(gtFile, 'r', encoding='unicode_escape') as data:
    #     datalist = data.readlines()
    with open(gtFile, 'r', encoding='utf-8') as data:
        datalist = data.readlines()
    # print(datalist)
    nSamples = len(datalist)
    for i in tqdm(range(nSamples)):
        imagePath, label = datalist[i].strip('\n').split('\t')
        imagePath = os.path.join(inputPath, imagePath)

        # # only use alphanumeric data
        # if re.search('[^a-zA-Z0-9]', label):
        #     continue

        if not os.path.exists(imagePath):
            print('%s does not exist' % imagePath)
            continue
        with open(imagePath, 'rb') as f:
            imageBin = f.read()
        if checkValid:
            try:
                if not checkImageIsValid(imageBin):
                    print('%s is not a valid image' % imagePath)
                    continue
            except:
                print('error occured', i)
                with open(outputPath + '/error_image_log.txt', 'a') as log:
                    log.write('%s-th image data occured error\n' % str(i))
                continue

        imageKey = 'image-%09d'.encode() % cnt
        labelKey = 'label-%09d'.encode() % cnt
        # print("a-imageKey", imageKey)
        # print("a-iableKey", labelKey)
        cache[imageKey] = imageBin
        cache[labelKey] = label.encode()

        if cnt % 1000 == 0:
            writeCache(env, cache)
            cache = {}
            # print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
    nSamples = cnt-1
    cache['num-samples'.encode()] = str(nSamples).encode()
    writeCache(env, cache)
    print('Created dataset with %d samples' % nSamples)


if __name__ == '__main__':
    fire.Fire(createDataset)
# python create_lmdb_dataset.py --inputPath D:/Additional_datasets/ --gtFile D:/Additional_datasets/gt_train.txt --outputPath data_lmdb/train
# python create_lmdb_dataset.py --inputPath D:/Additional_datasets/ --gtFile D:/Additional_datasets/gt_validation.txt --outputPath data_lmdb/validation
# python create_lmdb_dataset.py --inputPath D:/Additional_datasets/ --gtFile D:/Additional_datasets/gt_test.txt --outputPath data_lmdb/test