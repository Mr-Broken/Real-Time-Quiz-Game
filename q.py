import csv
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)

class MCQ():
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    def updates(self,cursor,bboxs):
        for x, bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userAns = x+1
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),cv2.FILLED)





#import csv file data
pathCSV = "mcq.csv"
with open(pathCSV,newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
print(dataAll)


# Creates Object for each MCQ
mcqlist = []
for q in dataAll:
    mcqlist.append(MCQ(q))
print(len(mcqlist))

print("Total MCQ objects Created :",len(mcqlist))

qNo = 0
qTotal = len(dataAll)
print(qTotal)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal:
        mcq = mcqlist[qNo]


        img, bbox = cvzone.putTextRect(img, mcq.question, [50, 100], 2, 2, offset=15, border=2, colorR=(0, 0, 0), colorB=(0, 0, 255))
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [50, 200], 2, 2, offset=15, border=2, colorR=(0, 0, 0), colorB=(0, 0, 255))
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 200], 2, 2, offset=15, border=2, colorR=(0, 0, 0), colorB=(0, 0, 255))
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [50, 300], 2, 2, offset=15, border=2, colorR=(0, 0, 0), colorB=(0, 0, 255))
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 300], 2, 2, offset=15, border=2, colorR=(0, 0, 0), colorB=(0, 0, 255))

        if hands:
            lmList = hands[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8],lmList[12])

            if length < 60:
                mcq.updates(cursor, [bbox1, bbox2, bbox3, bbox4])
                print(mcq.userAns)
                time.sleep(0.3)
                if mcq.userAns is not None:
                    qNo += 1
    else:
        score=0
        for mcq in mcqlist:
            if mcq.answer == mcq.userAns:
                score += 1
        score = round((score/qTotal)*100,2)
        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=15, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=15, border=5)
    #Draw Progess Bar
    barValue = 150 + (950//qTotal)*qNo
    cv2.rectangle(img, (150, 600), (barValue, 650),(0 , 255 ,0), cv2.FILLED)
    cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    img, _ = cvzone.putTextRect(img, f'{round((qNo/qTotal)*100)}%', [1130, 635], 2, 2, offset=16)


    cv2.imshow("Img", img)
    cv2.waitKey(1)
