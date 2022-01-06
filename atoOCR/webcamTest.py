import cv2

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3072)
# 연구실 웹캠의 최대 해상도는 fhd입니다 1920x1080
# cap=cap.set(3, 720)
# cap=cap.set(4, 1080)


print('width :%d, height : %d' % (cap.get(3), cap.get(4)))

while(True):
    ret, frame = cap.read()    # Read 결과와 frame

    if(ret) :
        # gray = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환
        # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        cv2.imshow('frame_color', frame)    # 컬러 화면 출력
        # cv2.imshow('frame_gray', gray)    # Gray 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()