import cv2
import numpy as np
import face_recognition
import os
import sys
a=sys.argv[1]
b=sys.argv[2]
print(a,b)

from datetime import datetime
ctr=0
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            date=now.date()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString},{date},{a},{b}')
 

 
encodeListKnown = findEncodings(images)
print('Encoding Complete')
 
cap = cv2.VideoCapture(0)
 
while True:
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break 
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
 
        if matches[matchIndex]:
            
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            # faceLoc = (y1, x2, y2, x1)
            # faceRegion = img[y1:y2, x1:x2]
            # # filename = 'face_region{}.jpg'.format(str(datetime.now()).split()[0]+str(datetime.now()).split()[1])
            # cv2.imwrite("Unknown\\temp"+str(ctr)+".jpg", faceRegion) 
            # ctr+=1
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
            markAttendance(name)
        else: 
            name = "UNKNOWN"
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            faceLoc = (y1, x2, y2, x1)
            faceRegion = img[y1:y2, x1:x2]
            # filename = 'face_region{}.jpg'.format(str(datetime.now()).split()[0]+str(datetime.now()).split()[1])
            cv2.imwrite("Unknown\\temp"+str(ctr)+".jpg", faceRegion) 
            ctr+=1
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            
 
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
