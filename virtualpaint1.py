import cv2
import numpy as np
framewidth=480
frameheight=360
cap=cv2.VideoCapture(0)

cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,1500)

myColors=[[111,84,104,133,210,255],
          [8,88,153,75,178,221],
           [36,74,136,63,254,255]]
mycolorvalue=[[236,32,27],
              [20,92,247],
              [20,247,45]]
mypoint=[]
def findcolor(img,myColors,mycolorvalue):
    imghsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoint=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imghsv, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgresult,(x,y),10,mycolorvalue[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoint.append([x,y,count])
        count+=1
    return newpoint
        #cv2.imshow(str(color[0]), mask)

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if(area>200):
            #cv2.drawContours(imgresult,cnt,-1,(,2)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
    return x+w//2,y
def drawoncanvas(mypoint,mycolorvalue):
      for point in mypoint:
          cv2.circle(imgresult, (point[0], point[1]), 10, mycolorvalue[point[2]], cv2.FILLED)
while True:
    success, img=cap.read()
    imgresult=img.copy()
    newpoint=findcolor(img,myColors,mycolorvalue)
    if len(newpoint)!=0:
        for newp in newpoint:
            mypoint.append(newp)
    if len(mypoint)!=0:
        drawoncanvas(mypoint,mycolorvalue)
    cv2.imshow("result", imgresult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break