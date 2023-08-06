# original:https://github.com/pdhruv93/computer-vision/tree/main/fingers-count
# original is modified by takefuji
import mediapipe as mp
import cv2
import math
import numpy as np
from time import sleep
import time,os

Hands = mp.solutions.hands
Draw = mp.solutions.drawing_utils

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = Hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_handedness:
            label = results.multi_handedness[handNumber].classification[0].label  # label gives if hand is left or right
            #account for inversion in cam
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"

        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos, label])

            if draw:
                Draw.draw_landmarks(originalImage, hand, Hands.HAND_CONNECTIONS)
        return landMarkList

import math,re
from math import sqrt as Q
import pytesseract
from os import path
r=""

def ocr():
 if path.exists('r.png'):
  image = cv2.imread('r.png',cv2.COLOR_BGR2GRAY)
  blue = image[:,:,0]
  _, img = cv2.threshold(blue, thresh=250, maxval=255, type=cv2.THRESH_BINARY)
  img=cv2.resize(img,(120,90))
  #img=cv2.resize(img,(128,128))
  conf = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0Oo1lL2Zz345Ssb67>8<9qgP-~WwMm/Vv&()aAyn'
  text=pytesseract.image_to_string(img, config=conf)
  text=text.replace("O","0")
  text=text.replace("o","0")
  text=text.replace("l","1")
  text=text.replace("L","1")
  text=text.replace("Z","2")
  text=text.replace("z","2")
  text=text.replace("S","5")
  text=text.replace("s","5")
  text=text.replace("F","5")
  text=text.replace("b","6")
  text=text.replace("g","9")
  text=text.replace("q","9")
  text=text.replace("p","+")
  text=text.replace("P","+")
  text=text.replace("~","-")
  text=text.replace("W","-")
  text=text.replace("w","-")
  text=text.replace("M","*")
  text=text.replace("m","*")
  text=text.replace("V","/")
  text=text.replace("v","/")
  text=text.replace("&","**")
  text=text.replace("a","Q(")
  text=text.replace(">","Q(")
  text=text.replace("A",")")
  text=text.replace("y","(")
  text=text.replace("n","(")
  text=re.sub('[^0-9-+/*()Q]', '',text)
  try:
   r=str(eval(str(text)))
   return text
  except SyntaxError:
   return "input"
 else: return ""


handDetector = HandDetector(min_detection_confidence=0.7)
cam = cv2.VideoCapture(0)
size=(640,480)
out=cv2.VideoWriter('r.mp4',cv2.VideoWriter_fourcc(*'mp4v'),24,size)

x=100
y=100
xy=[]
chunk=[]
chunkc=0
ct=0
flag=0
duration=900
start=time.time()
leng=""

while (time.time()-start)<duration:
    status, image = cam.read()
    image=cv2.flip(image,1)
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count=0
    if(len(handLandmarks) != 0):
# handLandmarks[point of 21 points][x or y] locates finger positions.
# see details: https://google.github.io/mediapipe/solutions/hands
# handLandmarks[4][1] 4->Thumb_tip 1->x-axis
# handLandmarks[8][2] 8->Index_finger_tip 2->y-axis
        x=handLandmarks[8][1]
        y=handLandmarks[8][2]

        if handLandmarks[4][1]+50 < handLandmarks[5][1]:       #Thumb finger
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            count = count+1
    ct=0
    try:
     if count==1:
      x=handLandmarks[8][1]
      y=handLandmarks[8][2]
      xy.append((x,y))
      for i in range(len(xy)-1):
       cv2.line(image,xy[i],xy[i+1],(255, 0, 0), 5)
      cv2.waitKey(1)
      sleep(0.1)
     elif count==4:
      sleep(0.1)
      ct=4
     elif count==3:
      sleep(0.1)
      ct=3
     elif count==5 or count==0:
      xy=xy
      cv2.waitKey(1)
     elif count==2:
      chunk.append(xy)
      chunkc=chunkc+1
      xy=[]
      x=handLandmarks[8][1]
      y=handLandmarks[8][2]
      xy.append((x,y))
      for i in range(len(xy)-1):
       cv2.line(image,xy[i],xy[i+1],(255, 0, 0), 5)
      cv2.waitKey(1)
      sleep(0.1)
    except IndexError:
     xy=xy
    cv2.putText(image, str(count), (45, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)
    for i in range(len(chunk)):
     for j in range(len(chunk[i])-1):
      cv2.line(image, chunk[i][j],chunk[i][j+1],(255, 0, 0), 10)
    cv2.moveWindow('result',10,10)
    cv2.imshow('result',image)
    out.write(image)
    cv2.waitKey(100)
    if ct==4:
     cv2.moveWindow('result',10,10)
     cv2.imshow('result',image)
     cv2.waitKey(100)
     cv2.imwrite('r.png',image)
     leng=ocr()
     #cv2.putText(image,str(leng), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 10)
     if leng=="input":
      cv2.putText(image,"AI unrecognizes", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
      ct=3
      leng=""
     else:
      if len(leng)>0:
       cv2.putText(image,str(leng)+"="+str(eval((leng))), (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 10)
       cv2.waitKey(200)
     cv2.imshow('result',image)
     cv2.imwrite('result.png',image)
     cv2.waitKey(100)
     out.write(image)
     flag=flag+1
    if ct==3:
     xy=[]
     if len(chunk)>0:
      for i in range(int(len(chunk)/20)):
       chunk.pop()
       chunkc=chunkc-1
    if ct==4 and flag>18:
     cv2.waitKey(100)
     xy=[]
     chunk=[]
     chunkc=0
     flag=0
     r=cv2.imread('result.png')
     cv2.imshow('final',r)
     cv2.waitKey(5000)
     out.release()
     cv2.destroyAllWindows()
     os._exit(0)
