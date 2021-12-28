# -*- coding: utf-8 -*-
import string
import argparse

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F

from utils import CTCLabelConverter, AttnLabelConverter
from dataset import RawDataset, AlignCollate
from model import Model
from craftPytorch import cDemo
from PIL import ImageFont, ImageDraw, Image
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import cv2
import numpy as np
import shutil
import time
def setModel(opt):
    start=time.time()
    """ model configuration """
    if 'CTC' in opt.Prediction:
        converter = CTCLabelConverter(opt.character)
    else:
        converter = AttnLabelConverter(opt.character)
    opt.num_class = len(converter.character)

    if opt.rgb:
        opt.input_channel = 3
    model = Model(opt)
    # print('model input parameters', opt.imgH, opt.imgW, opt.num_fiducial, opt.input_channel, opt.output_channel,
    #       opt.hidden_size, opt.num_class, opt.batch_max_length, opt.Transformation, opt.FeatureExtraction,
    #       opt.SequenceModeling, opt.Prediction)
    model = torch.nn.DataParallel(model).to(device)

    # load model
    # print('loading pretrained model from %s' % opt.saved_model)
    print("text recognition model load",time.time()-start)
    model.load_state_dict(torch.load(opt.saved_model, map_location=device))
    return (model,converter)



def demo(opt,model):
    model,converter=model
    # prepare data. two demo images from https://github.com/bgshih/crnn#run-demo
    AlignCollate_demo = AlignCollate(imgH=opt.imgH, imgW=opt.imgW, keep_ratio_with_pad=opt.PAD)
    demo_data = RawDataset(root=opt.image_folder, opt=opt)  # use RawDataset
    # print("dataLoader batch size",opt.batch_size)
    demo_loader = torch.utils.data.DataLoader(
        demo_data, batch_size=opt.batch_size,
        shuffle=False,
        # num_workers=int(opt.workers),
        num_workers=int(0),
        collate_fn=AlignCollate_demo, pin_memory=True)
    # print(demo_loader)
    # predict
    model.eval()
    cnt=0
    texts=[]
    with torch.no_grad():
        for image_tensors, image_path_list in demo_loader:
            # print(cnt)
            # craftTest(demo_data.__getitem__(cnt)[1])
            # cnt+=1
            # print(image_path_list)

            batch_size = image_tensors.size(0)
            image = image_tensors.to(device)

            # For max length prediction
            length_for_pred = torch.IntTensor([opt.batch_max_length] * batch_size).to(device)
            text_for_pred = torch.LongTensor(batch_size, opt.batch_max_length + 1).fill_(0).to(device)

            if 'CTC' in opt.Prediction:
                # print(image)
                # print(type(model))
                preds = model(image, text_for_pred)
                # print("여기1")
                # Select max probabilty (greedy decoding) then decode index to character
                preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                _, preds_index = preds.max(2)
                # preds_index = preds_index.view(-1)
                preds_str = converter.decode(preds_index, preds_size)

            else:
                preds = model(image, text_for_pred, is_train=False)
                # select max probabilty (greedy decoding) then decode index to character
                _, preds_index = preds.max(2)
                preds_str = converter.decode(preds_index, length_for_pred)

            # log = open(f'./log_demo_result.txt', 'a')
            dashed_line = '-' * 80
            head = f'{"image_path":25s}\t{"predicted_labels":25s}\tconfidence score'

            # print(f'{dashed_line}\n{head}\n{dashed_line}')
            # log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)
            for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):
                if 'Attn' in opt.Prediction:
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                    pred_max_prob = pred_max_prob[:pred_EOS]

                # calculate confidence score (= multiply of pred_max_prob)
                confidence_score = pred_max_prob.cumprod(dim=0)[-1]
                texts.append(pred)
                # print(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}')
                # log.write(f'{img_name:25s}\t{pred:25s}\t{confidence_score:0.4f}\n')

            # log.close()
    # print('-' * 80)
    # print(texts)
    del texts[len(texts)-1]
    return texts
import pathlib
import os
def saveCraftResult(dirPath,imgs,img):
    cnt=0
    for i in imgs:
        savePath= os.path.join(dirPath, str(cnt)+".jpg")
        cv2.imwrite(savePath,i)
        cnt+=1
    savePath = os.path.join(dirPath, "result" + ".jpg")
    cv2.imwrite(savePath, img)

    #
    # ROOT_DIR = dirPath
    # image1 = pathlib.Path(os.path.join(ROOT_DIR))
    # image_list = list(image1.glob('*.jpg'))
    # 이건 실험 코드 175부터
def getCraftResult(imagePath,craftModel):
    imgs, img,points = cDemo.main(imagePath,craftModel)
    # print(len(imgs))
    resultImgs=[]
    cnt=0
    for i in imgs:
        rows,cols,_=i.shape
        if(rows != 0 and cols != 0):
            # print(i.shape)
            resultImgs.append(i)
            # cv2.imshow("img",i)
            # cv2.waitKey(0)
        else:
            del points[cnt]
            cnt-=1
        cnt+=1
    return resultImgs, img,points
def putText(img,points,texts):
    # print(len(points),len(texts))
    fontSize=64
    font = ImageFont.truetype('malgun.ttf', fontSize)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    for i in range(len(points)):
        point=points[i]
        text=texts[i]
        draw.text((point[1],point[0]), text, font=font, fill=(255, 0, 255, 0))
        # cv2.putText는 한글안됨
        # cv2.putText(img, text, (point[1],point[0]), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 255), 5, cv2.LINE_AA)
    img = np.array(img_pil)

    return img

def craftOperation(imgPath,craftModel,dirPath):
    imgs,img,points=getCraftResult(imgPath,craftModel)
    if not (os.path.isdir(dirPath)):
        os.makedirs(os.path.join(dirPath))
    saveCraftResult(dirPath,imgs,img)
    return img,points


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_folder', help='path to image_folder which contains text images')


    parser.add_argument('--workers', type=int, help='number of data loading workers', default=4)
    parser.add_argument('--batch_size', type=int, default=192, help='input batch size')
    parser.add_argument('--saved_model', required=True, help="path to saved_model to evaluation")
    """ Data processing """
    parser.add_argument('--batch_max_length', type=int, default=25, help='maximum-label-length')
    parser.add_argument('--imgH', type=int, default=32, help='the height of the input image')
    parser.add_argument('--imgW', type=int, default=100, help='the width of the input image')
    parser.add_argument('--rgb', action='store_true', help='use rgb input')
    parser.add_argument('--character', type=str,
                        default='0123456789abcdefghijklmnopqrstuvwxyz가각간갇갈감갑값갓강갖같갚갛개객걀걔거걱건걷걸검겁것겉게겨격겪견결겹경곁계고곡곤곧골곰곱곳공과관광괜괴굉교구국군굳굴굵굶굽궁권귀귓규균귤그극근글긁금급긋긍기긴길김깅깊까깍깎깐깔깜깝깡깥깨꺼꺾껌껍껏껑께껴꼬꼭꼴꼼꼽꽂꽃꽉꽤꾸꾼꿀꿈뀌끄끈끊끌끓끔끗끝끼낌나낙낚난날낡남납낫낭낮낯낱낳내냄냇냉냐냥너넉넌널넓넘넣네넥넷녀녁년념녕노녹논놀놈농높놓놔뇌뇨누눈눕뉘뉴늄느늑는늘늙능늦늬니닐님다닥닦단닫달닭닮담답닷당닿대댁댐댓더덕던덜덟덤덥덧덩덮데델도독돈돌돕돗동돼되된두둑둘둠둡둥뒤뒷드득든듣들듬듭듯등디딩딪따딱딴딸땀땅때땜떠떡떤떨떻떼또똑뚜뚫뚱뛰뜨뜩뜯뜰뜻띄라락란람랍랑랗래랜램랫략량러럭런럴럼럽럿렁렇레렉렌려력련렬렵령례로록론롬롭롯료루룩룹룻뤄류륙률륭르른름릇릎리릭린림립릿링마막만많말맑맘맙맛망맞맡맣매맥맨맵맺머먹먼멀멈멋멍멎메멘멩며면멸명몇모목몬몰몸몹못몽묘무묵묶문묻물뭄뭇뭐뭘뭣므미민믿밀밉밌및밑바박밖반받발밝밟밤밥방밭배백뱀뱃뱉버번벌범법벗베벤벨벼벽변별볍병볕보복볶본볼봄봇봉뵈뵙부북분불붉붐붓붕붙뷰브븐블비빌빔빗빚빛빠빡빨빵빼뺏뺨뻐뻔뻗뼈뼉뽑뿌뿐쁘쁨사삭산살삶삼삿상새색샌생샤서석섞선설섬섭섯성세섹센셈셋셔션소속손솔솜솟송솥쇄쇠쇼수숙순숟술숨숫숭숲쉬쉰쉽슈스슨슬슴습슷승시식신싣실싫심십싯싱싶싸싹싼쌀쌍쌓써썩썰썹쎄쏘쏟쑤쓰쓴쓸씀씌씨씩씬씹씻아악안앉않알앓암압앗앙앞애액앨야약얀얄얇양얕얗얘어억언얹얻얼엄업없엇엉엊엌엎에엔엘여역연열엷염엽엿영옆예옛오옥온올옮옳옷옹와완왕왜왠외왼요욕용우욱운울움웃웅워원월웨웬위윗유육율으윽은을음응의이익인일읽잃임입잇있잊잎자작잔잖잘잠잡잣장잦재쟁쟤저적전절젊점접젓정젖제젠젯져조족존졸좀좁종좋좌죄주죽준줄줌줍중쥐즈즉즌즐즘증지직진질짐집짓징짙짚짜짝짧째쨌쩌쩍쩐쩔쩜쪽쫓쭈쭉찌찍찢차착찬찮찰참찻창찾채책챔챙처척천철첩첫청체쳐초촉촌촛총촬최추축춘출춤춥춧충취츠측츰층치칙친칠침칫칭카칸칼캄캐캠커컨컬컴컵컷케켓켜코콘콜콤콩쾌쿄쿠퀴크큰클큼키킬타탁탄탈탑탓탕태택탤터턱턴털텅테텍텔템토톤톨톱통퇴투툴툼퉁튀튜트특튼튿틀틈티틱팀팅파팎판팔팝패팩팬퍼퍽페펜펴편펼평폐포폭폰표푸푹풀품풍퓨프플픔피픽필핏핑하학한할함합항해핵핸햄햇행향허헌험헤헬혀현혈협형혜호혹혼홀홈홉홍화확환활황회획횟횡효후훈훌훔훨휘휴흉흐흑흔흘흙흡흥흩희흰히힘?!',
                        help='character label')
    parser.add_argument('--sensitive', action='store_true', help='for sensitive character mode')
    parser.add_argument('--PAD', action='store_true', help='whether to keep ratio then pad for image resize')
    """ Model Architecture """
    parser.add_argument('--Transformation', type=str, required=True, help='Transformation stage. None|TPS')
    parser.add_argument('--FeatureExtraction', type=str, required=True, help='FeatureExtraction stage. VGG|RCNN|ResNet')
    parser.add_argument('--SequenceModeling', type=str, required=True, help='SequenceModeling stage. None|BiLSTM')
    parser.add_argument('--Prediction', type=str, required=True, help='Prediction stage. CTC|Attn')
    parser.add_argument('--num_fiducial', type=int, default=20, help='number of fiducial points of TPS-STN')
    parser.add_argument('--input_channel', type=int, default=1, help='the number of input channel of Feature extractor')
    parser.add_argument('--output_channel', type=int, default=512,
                        help='the number of output channel of Feature extractor')
    parser.add_argument('--hidden_size', type=int, default=256, help='the size of the LSTM hidden state')
    print(torch.cuda.get_device_name(0))
    print("cuda is available ", torch.cuda.is_available())
    opt = parser.parse_args()
    print(opt)
    print(type(opt))
    # os.system("pause")

    """ vocab / character number configuration """
    if opt.sensitive:
        opt.character = string.printable[:-6]  # same with ASTER setting (use 94 char).

    cudnn.benchmark = True
    cudnn.deterministic = True
    opt.num_gpu = torch.cuda.device_count()
    # print(opt.image_folder)

    imgPath = "./demo_image3/demo_6.jpg"
    opt.image_folder = "./temps" #craft로 분리된 문자열이 저장되는 곳입니다
    craftModel=cDemo.loadModel()
    model = setModel(opt)


    time1=time.time()
    img,points=craftOperation(imgPath,craftModel,dirPath=opt.image_folder)
    time1 = time.time()-time1
    print("craft elapsed Time",time1)
    time2 = time.time()
    # cv2.imshow("img",img)
    # cv2.waitKey(0)
    texts=demo(opt,model)
    time2 = time.time() - time2
    # putText(points, ["1", "2", "3", "4", "5", "6", "7"])

    img=putText(img,points, texts)
    print("craft", time1)
    print("deep-text...", time2)
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", img)
    cv2.waitKey(0)
    shutil.rmtree(opt.image_folder)


# python demo3.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction CTC --image_folder demo_image2/ --saved_model best_accuracy.pth --imgH 64 --imgW 200

#첫번째
# python -m cProfile -o demo3.prof demo3.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction CTC --image_folder demo_image3/ --saved_model best_accuracy.pth --imgH 64 --imgW 200
#두번쨰
# python demo3.py --Transformation TPS --FeatureExtraction RCNN --SequenceModeling BiLSTM --Prediction Attn --image_folder demo_image2/ --saved_model best_accuracy2.pth --imgH 64 --imgW 200
#제공하는
# python demo3.py --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn --image_folder demo_image2/ --saved_model TPS-ResNet-BiLSTM-Attn.pth --imgH 64 --imgW 200

