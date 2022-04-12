# -*- coding: utf-8 -*-
import string
import argparse

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP
from utils import CTCLabelConverter, AttnLabelConverter
from dataset import RawDataset, AlignCollate
from model import Model
from craftPytorch import craft_demo
from PIL import ImageFont, ImageDraw, Image
import os
# os.environ["CUDA_VISIBLE_DEVICES"]="0"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
import cv2
import numpy as np
import shutil
import time

def setRecognitionModel(opt):
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
#     model = torch.nn.DataParallel(model).to(device)
#     print("device",device)
#     model.to(device)
#     model = torch.nn.DataParallel(model).to(device)
    print("device:",device,str(device))
#     print(torch.device())
#     device = torch.device('cuda:0,1' if torch.cuda.is_available() else "cpu")
    model = torch.nn.DataParallel(model,device_ids=[0,1])
    model.to(device)
    

    # load model
    # print('loading pretrained model from %s' % opt.saved_model)
    model.load_state_dict(torch.load(opt.saved_model, map_location=device))
#     print(opt.saved_model)
#     print(torch.load(opt.saved_model, map_location=device))
#     checkpoint = torch.load(opt.saved_model, map_location=device)
#     for key in list(checkpoint.keys()):
#         if 'model.' in key:
#             checkpoint[key.replace('model.', '')] = checkpoint[key]
#             del checkpoint[key]
#     model.load_state_dict(checkpoint)




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
#         num_workers=int(opt.workers),
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
        # cv2.imshow(str(cnt), i)
        savePath= os.path.join(dirPath, str(cnt)+".jpg")
        cv2.imwrite(savePath,i)
        cnt+=1

    savePath = os.path.join(dirPath, "result" + ".jpg")
    cv2.imwrite(savePath, img)
    # print(savePath)

    # cv2.imshow("img", img)
    # cv2.waitKey(0)

    #
    # ROOT_DIR = dirPath
    # image1 = pathlib.Path(os.path.join(ROOT_DIR))
    # image_list = list(image1.glob('*.jpg'))
    # 이건 실험 코드 175부터
def getCraftResult(imagePath,craftModel):
    

    imgs, img,points = craft_demo.main(imagePath,craftModel)
    

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
    font = 64
    fontSize = 4032
    # print(img.shape)
    rows,cols,_=img.shape
    cnt=1
    tempSize=max(rows,cols)

    while(True):
        if(tempSize>(fontSize/cnt)):
            break
        else:
            cnt+=1
    # print("tempSize",font/cnt)
    font=int(font/cnt)
    font=10
    # fontSize=

    font = ImageFont.truetype('malgun.ttf', font)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    for i in range(len(points)):
        point=points[i]
        text=texts[i]
        draw.text((point[1],point[0]), text, font=font, fill=(0, 215, 255, 0))
        # cv2.putText는 한글안됨
        # cv2.putText(img, text, (point[1],point[0]), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 255), 5, cv2.LINE_AA)
    img = np.array(img_pil)

    return img

def craftOperation(imgPath,craftModel,dirPath):
    #print('craftOperation')
    imgs,img,points=getCraftResult(imgPath,craftModel)
    if not (os.path.isdir(dirPath)):
        os.makedirs(os.path.join(dirPath))
    saveCraftResult(dirPath,imgs,img)
    return img,points

def setModel():
    '''
    기존 파서를 이용한 방식은 실행 시 매번 터미널에 값을 입력해야하는 번거로움이 있습니다
    따라서 paser를 namespace로 변경하여 값 입력을 받지 않게 합니다
    해당 함수는 두가지 모델을 세팅하는 함수입니다.

    return
    '''
    opt = argparse.Namespace(
        image_folder=str("demo_image2/"),
        workers=int(4),
        batch_size=int(192),
        saved_model=str('best_accuracy.pth'),
        batch_max_length=int(25),
        imgH=int(64),
        imgW=int(200),
        character=str(
            '0123456789abcdefghijklmnopqrstuvwxyz가각간갇갈갉갊감갑값갓갔강갖갗같갚갛개객갠갤갬갭갯갰갱갸갹갼걀걋걍걔걘걜거걱건걷걸걺검겁것겄겅겆겉겊겋게겐겔겜겝겟겠겡겨격겪견겯결겸겹겻겼경곁계곈곌곕곗고곡곤곧골곪곬곯곰곱곳공곶과곽관괄괆괌괍괏광괘괜괠괩괬괭괴괵괸괼굄굅굇굉교굔굘굡굣구국군굳굴굵굶굻굼굽굿궁궂궈궉권궐궜궝궤궷귀귁귄귈귐귑귓규균귤그극근귿글긁금급긋긍긔기긱긴긷길긺김깁깃깅깆깊까깍깎깐깔깖깜깝깟깠깡깥깨깩깬깰깸깹깻깼깽꺄꺅꺌꺼꺽꺾껀껄껌껍껏껐껑께껙껜껨껫껭껴껸껼꼇꼈꼍꼐꼬꼭꼰꼲꼴꼼꼽꼿꽁꽂꽃꽈꽉꽐꽜꽝꽤꽥꽹꾀꾄꾈꾐꾑꾕꾜꾸꾹꾼꿀꿇꿈꿉꿋꿍꿎꿔꿜꿨꿩꿰꿱꿴꿸뀀뀁뀄뀌뀐뀔뀜뀝뀨끄끅끈끊끌끎끓끔끕끗끙끝끼끽낀낄낌낍낏낑나낙낚난낟날낡낢남납낫났낭낮낯낱낳내낵낸낼냄냅냇냈냉냐냑냔냘냠냥너넉넋넌널넒넓넘넙넛넜넝넣네넥넨넬넴넵넷넸넹녀녁년녈념녑녔녕녘녜녠노녹논놀놂놈놉놋농높놓놔놘놜놨뇌뇐뇔뇜뇝뇟뇨뇩뇬뇰뇹뇻뇽누눅눈눋눌눔눕눗눙눠눴눼뉘뉜뉠뉨뉩뉴뉵뉼늄늅늉느늑는늘늙늚늠늡늣능늦늪늬늰늴니닉닌닐닒님닙닛닝닢다닥닦단닫달닭닮닯닳담답닷닸당닺닻닿대댁댄댈댐댑댓댔댕댜더덕덖던덛덜덞덟덤덥덧덩덫덮데덱덴델뎀뎁뎃뎄뎅뎌뎐뎔뎠뎡뎨뎬도독돈돋돌돎돐돔돕돗동돛돝돠돤돨돼됐되된될됨됩됫됴두둑둔둘둠둡둣둥둬뒀뒈뒝뒤뒨뒬뒵뒷뒹듀듄듈듐듕드득든듣들듦듬듭듯등듸디딕딘딛딜딤딥딧딨딩딪따딱딴딸텭땀땁땃땄땅땋때땍땐땔땜땝땟땠땡떠떡떤떨떪떫떰떱떳떴떵떻떼떽뗀뗄뗌뗍뗏뗐뗑뗘뗬또똑똔똘똥똬똴뙈뙤뙨뚜뚝뚠뚤뚫뚬뚱뛔뛰뛴뛸뜀뜁뜅뜨뜩뜬뜯뜰뜸뜹뜻띄띈띌띔띕띠띤띨띰띱띳띵라락란랄람랍랏랐랑랒랖랗퇏래랙랜랠램랩랫랬랭랴략랸럇량러럭런럴럼럽럿렀렁렇레렉렌렐렘렙렛렝려력련렬렴렵렷렸령례롄롑롓로록론롤롬롭롯롱롸롼뢍뢨뢰뢴뢸룀룁룃룅료룐룔룝룟룡루룩룬룰룸룹룻룽뤄뤘뤠뤼뤽륀륄륌륏륑류륙륜률륨륩툩륫륭르륵른를름릅릇릉릊릍릎리릭린릴림립릿링마막만많맏말맑맒맘맙맛망맞맡맣매맥맨맬맴맵맷맸맹맺먀먁먈먕머먹먼멀멂멈멉멋멍멎멓메멕멘멜멤멥멧멨멩며멱면멸몃몄명몇몌모목몫몬몰몲몸몹못몽뫄뫈뫘뫙뫼묀묄묍묏묑묘묜묠묩묫무묵묶문묻물묽묾뭄뭅뭇뭉뭍뭏뭐뭔뭘뭡뭣뭬뮈뮌뮐뮤뮨뮬뮴뮷므믄믈믐믓미믹민믿밀밂밈밉밋밌밍및밑바박밖밗반받발밝밞밟밤밥밧방밭배백밴밸뱀뱁뱃뱄뱅뱉뱌뱍뱐뱝버벅번벋벌벎범법벗벙벚베벡벤벧벨벰벱벳벴벵벼벽변별볍볏볐병볕볘볜보복볶본볼봄봅봇봉봐봔봤봬뵀뵈뵉뵌뵐뵘뵙뵤뵨부북분붇불붉붊붐붑붓붕붙붚붜붤붰붸뷔뷕뷘뷜뷩뷰뷴뷸븀븃븅브븍븐블븜븝븟비빅빈빌빎빔빕빗빙빚빛빠빡빤빨빪빰빱빳빴빵빻빼빽뺀뺄뺌뺍뺏뺐뺑뺘뺙뺨뻐뻑뻔뻗뻘뻠뻣뻤뻥뻬뼁뼈뼉뼘뼙뼛뼜뼝뽀뽁뽄뽈뽐뽑뽕뾔뾰뿅뿌뿍뿐뿔뿜뿟뿡쀼쁑쁘쁜쁠쁨쁩삐삑삔삘삠삡삣삥사삭삯산삳살삵삶삼삽삿샀상샅새색샌샐샘샙샛샜생샤샥샨샬샴샵샷샹섀섄섈섐섕서석섞섟선섣설섦섧섬섭섯섰성섶세섹센셀셈셉셋셌셍셔셕션셜셤셥셧셨셩셰셴셸솅소속솎손솔솖솜솝솟송솥솨솩솬솰솽쇄쇈쇌쇔쇗쇘쇠쇤쇨쇰쇱쇳쇼쇽숀숄숌숍숏숑수숙순숟술숨숩숫숭숯숱숲숴쉈쉐쉑쉔쉘쉠쉥쉬쉭쉰쉴쉼쉽쉿슁슈슉슐슘슛슝스슥슨슬슭슴습슷승시식신싣실싫심십싯싱싶싸싹싻싼쌀쌈쌉쌌쌍쌓쌔쌕쌘쌜쌤쌥쌨쌩썅써썩썬썰썲썸썹썼썽쎄쎈쎌쏀쏘쏙쏜쏟쏠쏢쏨쏩쏭쏴쏵쏸쐈쐐쐤쐬쐰쐴쐼쐽쑈쑤쑥쑨쑬쑴쑵쑹쒀쒔쒜쒸쒼쓩쓰쓱쓴쓸쓺쓿씀씁씌씐씔씜씨씩씬씰씸씹씻씽아악안앉않알앍앎앓암압앗았앙앝앞애액앤앨앰앱앳앴앵야약얀얄얇얌얍얏양얕얗얘얜얠얩어억언얹얻얼얽얾엄업없엇었엉엊엌엎에엑엔엘엠엡엣엥여역엮연열엶엷염엽엾엿였영옅옆옇예옌옐옘옙옛옜오옥온올옭옮옰옳옴옵옷옹옻와왁완왈왐왑왓왔왕왜왝왠왬왯왱외왹왼욀욈욉욋욍요욕욘욜욤욥욧용우욱운울욹욺움웁웃웅워웍원월웜웝웠웡웨웩웬웰웸웹웽위윅윈윌윔윕윗윙유육윤율윰윱윳융윷으윽은을읊음읍읏응읒읓읔읕읖읗의읜읠읨읫이익인일읽읾잃임입잇있잉잊잎자작잔잖잗잘잚잠잡잣잤장잦재잭잰잴잼잽잿쟀쟁쟈쟉쟌쟎쟐쟘쟝쟤쟨쟬저적전절젊점접젓정젖제젝젠젤젬젭젯젱져젼졀졈졉졌졍졔조족존졸졺좀좁좃종좆좇좋좌좍좔좝좟좡좨좼좽죄죈죌죔죕죗죙죠죡죤죵주죽준줄줅줆줌줍줏중줘줬줴쥐쥑쥔쥘쥠쥡쥣쥬쥰쥴쥼즈즉즌즐즘즙즛증지직진짇질짊짐집짓징짖짙짚짜짝짠짢짤짧짬짭짯짰짱째짹짼쨀쨈쨉쨋쨌쨍쨔쨘쨩쩌쩍쩐쩔쩜쩝쩟쩠쩡쩨쩽쪄쪘쪼쪽쫀쫄쫌쫍쫏쫑쫓쫘쫙쫠쫬쫴쬈쬐쬔쬘쬠쬡쭁쭈쭉쭌쭐쭘쭙쭝쭤쭸쭹쮜쮸쯔쯤쯧쯩찌찍찐찔찜찝찡찢찧차착찬찮찰참찹찻찼창찾채책챈챌챔챕챗챘챙챠챤챦챨챰챵처척천철첨첩첫첬청체첵첸첼쳄쳅쳇쳉쳐쳔쳤쳬쳰촁초촉촌촐촘촙촛총촤촨촬촹최쵠쵤쵬쵭쵯쵱쵸춈추축춘출춤춥춧충춰췄췌췐취췬췰췸췹췻췽츄츈츌츔츙츠측츤츨츰츱츳층치칙친칟칠칡침칩칫칭카칵칸칼캄캅캇캉캐캑캔캘캠캡캣캤캥캬캭컁커컥컨컫컬컴컵컷컸컹케켁켄켈켐켑켓켕켜켠켤켬켭켯켰켱켸코콕콘콜콤콥콧콩콰콱콴콸쾀쾅쾌쾡쾨쾰쿄쿠쿡쿤쿨쿰쿱쿳쿵쿼퀀퀄퀑퀘퀭퀴퀵퀸퀼큄큅큇큉큐큔큘큠크큭큰클큼큽킁키킥킨킬킴킵킷킹타탁탄탈탉탐탑탓탔탕태택탠탤탬탭탯탰탱탸턍터턱턴털턺텀텁텃텄텅테텍텐텔템텝텟텡텨텬텼톄톈토톡톤톨톰톱톳통톺톼퇀퇘퇴퇸툇툉툐투툭툰툴툼툽툿퉁퉈퉜퉤튀튁튄튈튐튑튕튜튠튤튬튱트특튼튿틀틂틈틉틋틔틘틜틤틥티틱틴틸팀팁팃팅파팍팎판팔팖팜팝팟팠팡팥패팩팬팰팸팹팻팼팽퍄퍅퍼퍽펀펄펌펍펏펐펑페펙펜펠펨펩펫펭펴편펼폄폅폈평폐폘폡폣포폭폰폴폼폽폿퐁퐈퐝푀푄표푠푤푭푯푸푹푼푿풀풂품풉풋풍풔풩퓌퓐퓔퓜퓟퓨퓬퓰퓸퓻퓽프픈플픔픕픗피픽핀필핌핍핏핑하학한할핥함합핫항해핵핸핼햄햅햇했행햐향허헉헌헐헒험헙헛헝헤헥헨헬헴헵헷헹혀혁현혈혐협혓혔형혜혠혤혭호혹혼홀홅홈홉홋홍홑화확환활홧황홰홱홴횃횅회획횐횔횝횟횡효횬횰횹횻후훅훈훌훑훔훗훙훠훤훨훰훵훼훽휀휄휑휘휙휜휠휨휩휫휭휴휵휸휼흄흇흉흐흑흔흖흗흘흙흠흡흣흥흩희흰흴흼흽힁히힉힌힐힘힙힛힝()%?!.\'\",'),
        Transformation=str('TPS'),
        FeatureExtraction=str('ResNet'),
        SequenceModeling=str('BiLSTM'),
        Prediction=str('CTC'),
        num_fiducial=int(20),
        input_channel=int(1),
        output_channel=int(512),
        hidden_size=int(256),
        rgb=False,
        sensitive=False,
        PAD=False
    )
    """ Model Architecture """

    print("\033[31mcuda is available ", torch.cuda.is_available())
    print("     gpu",torch.cuda.get_device_name(0))

    # print(opt, type(opt))

    # os.system("pause")
    """ vocab / character number configuration """
    if opt.sensitive:
        opt.character = string.printable[:-6]  # same with ASTER setting (use 94 char).

    cudnn.benchmark = True
    cudnn.deterministic = True
    opt.num_gpu = torch.cuda.device_count()
#     opt.num_gpu = 1
    print("num_gpu: ",opt.num_gpu)


    tempPath = "./temps"  # craft로 분리된 문자열이 저장되는 곳입니다
    mkdir(tempPath)
    opt.image_folder = tempPath
    # print("-"*50)
    # print(os.getcwd())
    # print("-" * 50)
    t1=time.time()
    torch.tensor(1).cuda(0).cuda(1)
    craftModel = craft_demo.loadModel()
    print("text detection model load, elapsed time:",time.time()-t1)
    t2 = time.time()
    model = setRecognitionModel(opt)
    print("text recognition model load, elapsed time:", time.time() - t2,'\033[0m')
    return craftModel,model, opt
def mkdir(path="./temps"):
    if os.path.exists(path):
        shutil.rmtree(path)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def endLineCHeck(i,datas,newText,newTexts):
    if (i >= len(datas) - 1):
        newText = sorted(newText, key=lambda x: (abs(x[1])))
        newText = [i[4] for i in newText]
        # os.system('pause')
        newTexts += ' '.join(newText) + '\n'
        return newTexts
    else:
        return newTexts

def separate_list(datas):
    check = False
    newTexts = ""
    newText = []
    i = 0
    # print("ocr result")
    # print(datas)
    # print("*" * 50)
    print("*" * 50)
    print("separate_list")
    for i, data in enumerate(datas):
        print(data,i,len(datas)-1)
        if (check == False):
            # 라인 시작 부분 체크
            check = True
            bdata = data
            newText.append(data)
            continue
        br1, bc1, br2, bc2, t1 = bdata
        r1, c1, r2, c2, t2 = data
        range1 = range(br1, br2 + 1)
        range2 = range(r1, r2 + 1)
        x = set(range1)
        x = x.intersection(range2)
        print("     교집합 원소수:",len(x), "기준 원소 수",len(range1) / 2.5)
        if (len(x) == 0):
            print(newText)
            newText = sorted(newText, key=lambda x: (abs(x[1])))
            newText=[i[4] for i in newText]
            # os.system('pause')
            newTexts += ' '.join(newText)+'\n'
            newText = []
            newText.append(data)
            bdata = data
            print("교집합 원소수:",len(x), "기준 원소 수",len(range1) / 2.5,"     분리1")
            newTexts=endLineCHeck(i=i,datas=datas,newText=newText,newTexts=newTexts)
        elif ((len(range1) / 2.5 >= len(x))):
            newText = sorted(newText, key=lambda x: (abs(x[1])))
            print(newText)
            newText = [i[4] for i in newText]
            newTexts += ' '.join(newText) + '\n'
            newText = []
            newText.append(data)
            bdata = data
            print("교집합 원소수:",len(x), "기준 원소 수",len(range1) / 2.5,"     분리2")
            newTexts=endLineCHeck(i=i,datas=datas,newText=newText,newTexts=newTexts)
        else:
            newText.append(data)
            newTexts=endLineCHeck(i=i,datas=datas,newText=newText,newTexts=newTexts)
    print("*"*50)
    print("lineResult")
    print(newTexts)
    return newTexts




def groupby_api(points,texts):


    #포인트들에 텍스트 추가 (1,3,2,3,타이레놀)
    print("*" * 50)
    print("ocrResult")
    datas=[(*points[i],texts[i]) for i in range(len(texts))]
    print(datas)
    print("*"*50)
    print("sorting by y2")
    datas=sorted(datas,key = lambda x : (x[2]))
    print(datas)
    print("*" * 50)
    print("sorting by multiple criteria(y2,x2)")
    # datas = sorted(datas, key=lambda x: (x[2],x[3]))
    # print(datas)

    # os.system('pause')
    newTexts=separate_list(datas)
        # if( (r1>=br1 and r1<=br2) )

    return newTexts


if __name__ == '__main__':
    name="003"
    # imgPath = "C:/Users/dgdgk/Desktop/atomom_product_server/cosmetic_demo_image/"+name+".jpg"
    #imgPath= "C:/Users/dgdgk/Desktop/atomom_product_server/test_image/"+name+".jpg"

    imgPath= "../roi/016.jpg"
#     imgPath= "../demo_image/1.jpg"
    img=cv2.imread(imgPath);
    
    craftModel, model, opt = setModel()
    t1=time.time()
    img,points=craftOperation(imgPath,craftModel,dirPath=opt.image_folder)


    # print(points)
    #
    # rows, cols, _ = img.shape
    # zeros = np.zeros((rows, cols), dtype=np.uint8)
    # for i in points:
    #     y1, x1, y2, x2 = i
    #     cv2.rectangle(zeros, (x1, y1), (x2, y2), (255, 0, 0), 5)
    # cum = []
    # x, y = np.where(zeros == 255)
    # for i, data in enumerate(x):
    #     zeros[x[i], y[i]] = 255
    #     cum.append([y[i], x[i]])
    # np.save('C:/Users/dgdgk/Documents/text/'+name, zeros)


    texts=demo(opt,model)
#     groupby_api(points,texts)
    print(texts)
    print(time.time()-t1)

    # img=putText(img,points, texts)
    #
    #
    # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    # cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    # cv2.imshow("img", img)
    # cv2.imshow(name, zeros)
    # cv2.waitKey(0)


