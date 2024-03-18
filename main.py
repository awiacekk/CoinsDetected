import math

import cv2 as cv
import numpy as np

img = cv.imread("tray1.jpg", cv.IMREAD_COLOR)
width = int(img.shape[1] * 80 / 100)
height = int(img.shape[0] * 80 / 100)
dim = (width, height)
#img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
#gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

blur = cv.GaussianBlur(img, (11, 11), 0)
gaus = cv.Canny(blur, 50, 180)
kernel = np.ones((3,3),np.uint8)
gaus = cv.dilate(gaus, kernel, iterations=1)
gaus = cv.morphologyEx(gaus, cv.MORPH_OPEN, kernel)
gaus = cv.morphologyEx(gaus, cv.MORPH_CLOSE, kernel)
circles = cv.HoughCircles(gaus,cv.HOUGH_GRADIENT,1,20, param1=130,param2=30,minRadius=0,maxRadius=50)
#edges = cv.Canny(gaus,50,180,apertureSize = 3)
lines = cv.HoughLinesP(gaus,1,np.pi/180,90, minLineLength=100, maxLineGap=5)
coorX1 = []
coorX2 = []
coorY1 = []
coorY2 = []
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    coorX1.append(x1)
    coorX2.append(x2)
    coorY1.append(y1)
    coorY2.append(y2)

circles = np.uint16(np.around(circles))
money = []
naTacy = 0
pozaTaca = 0
for i in circles[0,:]:
    money.append(i[2])

max = max(money)
c5 = []
c05 = []
wNaTacy = 0
wPozaTaca = 0
for i in circles[0,:]:
    if i[2] / max >= 0.92:
        cv.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
        c5.append(i[2])
    else:
        cv.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 2)
        cv.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
        c05.append(i[2])
    if i[0] < np.max(coorX2) and i[0] > np.min(coorX1) and i[1] > np.min(coorY1) and i[1] < np.max(coorY2):
        naTacy+=1
        if float(i[2]) / max > 0.92:
            wNaTacy+=5.0
        else:
            wNaTacy+=0.05
    else:
        pozaTaca+=1
        if float(i[2]) / max > 0.92:
            wPozaTaca+=5.0
        else:
            wPozaTaca+=0.05

cmX = round(((np.max(coorX2)-np.min(coorX1)) / max) * 1.2, 2)
cmY = round(((np.max(coorY2)-np.min(coorY1)) / max) * 1.2, 2)
print("Number of coins on the tray: "+str(naTacy)+", number of coins outside of the train "+str(pozaTaca))
print("Value of coins on the tray: "+str(wNaTacy)+", value of coins outside of the tray: "+str(wPozaTaca))
print("5zl: "+str(len(c5))+", 5gr: "+str(len(c05)))
print("Dimensions: "+str(cmX)+" x "+str(cmY)+" [cm]")

cv.imshow('Detected circles',img)
cv.waitKey(0)
cv.destroyAllWindows()