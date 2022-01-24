import csv
import os
from tqdm import tqdm

'''
    새로운 csv 형태                              원본 csv 형태
    0   : id                                    0  : id
    1   : korean                                1  : Allergy
    2   : oldKorean                             2  : Twenty
    3   : english                               3  : TwentyDetail
    4   : oldEnglish                            4  : Korean
    5   : hazardScoreMin                        5  : English
    6   : hazardScoreMax                        6  : Forbidden
    7   : dataAvailability                      7  : Purpose
    8   : allergy                               8  : Cosmedical
    9   : twenty                                9  : Limitation
    10  : twentyDetail                          10  : SkinType
    11  : goodForOily                           11 : SkinRemarkB
    12  : goodForSensitive                      12 : SkinRemarkG
    13  : goodForDry                            13 : EWG
    14  : badForOily                            14 : EWGDataAvailability
    15  : badForSensitive                       15 : EWGDataAvailabilityText
    16  : badForDry
    17  : skinRemarkG
    18  : skinRemarkB
    19  : Cosmedical
    20  : purpose
    21  : limitation
    22  : forbidden
'''

def operation(old,new):
    new[0] = old[0]
    new = korean_oldKorean(old, new)
    new[3] = old[5]
    new = ewg(old, new)
    new[7] = old[14]
    new[8] = old[1]
    new[9] = old[2]
    new[10] = old[3]
    new = skinType(old, new)
    new[17] = old[12]
    new[18] = old[11]
    new= cosmedical(old,new)
    new[20] =old[7]
    new[21] = old[9]
    new[22] = old[6]

    return new
    pass
def korean_oldKorean(old,new):
    korean=old[4]
    new[1]=korean
    if("(구명칭)" in korean):
        # print(korean)
        korean=korean.split(';',1)
        if(len(korean)>=2):
            new[1] = korean[0]
            new[2]=korean[1].replace('(구명칭)','')
        else:
            text=korean[0].replace('(구명칭)','')
            new[1]=text
            new[2]=text
    # print(new[1],new[2])
    return new
def ewg(old,new):
    score=old[13]
    score_min=score
    score_max=score
    # print(score,type(score))
    if ("_" in score):
        score = score.split('_', 1)
        score_min=score[0]
        score_max=score[1]
    new[5] = score_min
    new[6] = score_max
    return new

def skinType(old,new):
    sType=old[10]
    new[11]= '1' if ('go' in sType) else '0'
    new[12]= '1' if ('gs' in sType) else '0'
    new[13]= '1' if ('gd' in sType) else '0'
    new[14]= '1' if ('bo' in sType) else '0'
    new[15]= '1' if ('bs' in sType) else '0'
    new[16]= '1' if ('bd' in sType) else '0'
    return new

def cosmedical(old,new):
    status=old[8]
    # print("status",status)
    if (status == '1'): new[19] = "미백 개선 성분으로, 미백 개선에 도움이 돼요 :)"
    if (status == '2'): new[19] = "주름 개선 성분으로, 주름 개선에 도움이 돼요 :)"
    if (status == '3'): new[19] = "자외선 차단 성분입니다 :)"
    return new

if __name__ == '__main__':
    fr = open('data_parsed.csv', 'r', newline='', encoding='UTF-8-sig')
    fw = open('data_result.csv', 'w', newline='', encoding='UTF-8-sig')
    wr = csv.writer(fw)
    rdr = csv.reader(fr)
    lis=['id','korean','oldKorean','English','oldEnglish','hazardScoreMin','hazardScoreMax',
         'dataAvailability','allergy','twenty','twentyDetail','goodForOily','goodForSensitive','goodForDry',
         'badForOily','badForSensitive','badForDry','skinRemarkG','skinRemarkB','Cosmedical','purpose','limitation','forbidden'
         ]
    # print(lis)

    wr.writerow(lis)
    cnt=0
    for line in tqdm(rdr):
        if(cnt==0):
            cnt+=1
            continue
        old=line
        new = [None for i in range(23)]
        new=operation(old,new)
        wr.writerow(new)
        # for i,data in enumerate(new):
        #     print(lis[i],"                  ",data)
        # os.system('pause')
    fw.close()
    # st1="레이트"
    # st2="레이탈(구명칭)"
    #
    # print("(구명칭)" in st1)
    # print("(구명칭)" in st2)

    pass