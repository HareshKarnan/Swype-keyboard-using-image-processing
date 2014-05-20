image="keyboard.jpg"
ball="yellowball.png"
alphA="a.png"
pragyan=['p','r','a','g','y','a','n']
haresh=['h','a','r','e','s','h']
pranav=['p','r','a','n','a','v']
sangam=['s','a','n','g','a','m']
import enchant
from autopy import mouse

import cv,numpy
global imgshv
stack=list()
global x,y,x1,y1
x1,y1=0,0
char2='a'
#m.getthresholdedimg(im)
d=enchant.Dict("en_US")

def getthresholdedimg(im):

        '''this function take RGB image.Then convert it into HSV for easy colour detection and threshold it with yellow and blue part as white and all other regions as black.Then return that image'''
        global imghsv
        imghsv=cv.CreateImage(cv.GetSize(im),8,3)
        cv.CvtColor(im,imghsv,cv.CV_BGR2HSV)                                

        imgyellow=cv.CreateImage(cv.GetSize(im),8,1)
        imgblue=cv.CreateImage(cv.GetSize(im),8,1)

        imgthreshold=cv.CreateImage(cv.GetSize(im),8,1)

        cv.InRangeS(imghsv,cv.Scalar(20,100,100),cv.Scalar(30,255,255),imgyellow)        # Select a range of yellow color
        cv.InRangeS(imghsv,cv.Scalar(100,100,100),cv.Scalar(120,255,255),imgblue)        # Select a range of blue color
        cv.Add(imgyellow,imgblue,imgthreshold)
        return imgthreshold

#opencvpart.opencvdefinitions()

capture=cv.CaptureFromCAM(0)
frame = cv.QueryFrame(capture)
frame_size = cv.GetSize(frame)
test=cv.CreateImage(cv.GetSize(frame),8,3)
img2=cv.CreateImage(cv.GetSize(frame),8,3)


blue=[]
yellow=[]


import pygame,sys
from pygame.locals import *

pygame.init()
screen=pygame.display.set_mode((959,376),0,32)


keyboard=pygame.image.load(image).convert()
yellowball=pygame.image.load(ball).convert_alpha()
alphaAscreen=pygame.image.load(alphA).convert_alpha()

def learn(stack):
    count=0
    success=0
    for i in range(len(pragyan)):
        for j in range(len(stack)):
            if(pragyan[i]==stack[j]):
                count=count+1
                if(count==len(pragyan)):
                    return "pragyan"
                    success=1
                

def classify(x,y):
    char ='.'
    if 11<y<90 :
        if 7<x<77 :
            char='q'
        elif 94<x<163 :
            char='w'
        elif 182<x<252 :
            char='e'
        elif 268<x<338 :
            char='r'
        elif 356<x<425 :
            char='t'
        elif 443<x<513 :
            char='y'
        elif 531<x<599 :
            char='u'
        elif 618<x<685 :
            char='i'
        elif 705<x<772 :
            char='o'
        elif 792<x<861 :
            char='p'
    elif 104<y<179 :
        if 44<x<111 :
            char='a'
        elif 129<x<198 :
            char='s'
        elif 215<x<284 :
            char='d'
        elif 302<x<371 :
            char='f'
        elif 389<x<456 :
            char='g'
        elif 476<x<541 :
            char='h'
        elif 561<x<628 :
            char='j'
        elif 647<x<714 :
            char='k'
        elif 732<x<801 :
            char='l'
    elif 196<y<271 :
        if 92<x<160 :
            char='z'
        elif 178<x<244 :
            char='x'
        elif 263<x<329 :
            char='c'
        elif 349<x<412 :
            char='v'
        elif 431<x<499 :
            char='b'
        elif 517<x<583 :
            char='n'
        elif 602<x<668 :
            char='m'
    elif 288<y<363 :
        if 263<x<752 :
            char=' '
    return char
        
"""def machinelearningalgo(stack):
    
    for i in range(len(stack)):
        if(stack[i]==1)"""
while(1):
    #m.whilerun()
    
    color_image = cv.QueryFrame(capture)
    imdraw=cv.CreateImage(cv.GetSize(frame),8,3)
    cv.SetZero(imdraw)
    cv.Flip(color_image,color_image,1)
    cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)
    imgyellowthresh=getthresholdedimg(color_image)
    cv.Erode(imgyellowthresh,imgyellowthresh,None,3)
    cv.Dilate(imgyellowthresh,imgyellowthresh,None,10)
    img2=cv.CloneImage(imgyellowthresh)
    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(imgyellowthresh, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
    points = []

#        This is the new part here. ie Use of cv.BoundingRect()
    while contour:
            # Draw bounding rectangles
            bound_rect = cv.BoundingRect(list(contour))
            contour = contour.h_next()
            # for more details about cv.BoundingRect,see documentation
            pt1 = (bound_rect[0], bound_rect[1])
            pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
            points.append(pt1)
            points.append(pt2)
            cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

    #        Calculating centroids

            centroidx=cv.Round((pt1[0]+pt2[0])/2)
            centroidy=cv.Round((pt1[1]+pt2[1])/2)

    #        Identifying if blue or yellow blobs and adding centroids to corresponding lists
            if (20<cv.Get2D(imghsv,centroidy,centroidx)[0]<30):
                    yellow.append((centroidx,centroidy))
            elif (100<cv.Get2D(imghsv,centroidy,centroidx)[0]<120):
                    blue.append((centroidx,centroidy))

#                 Now drawing part. Exceptional handling is used to avoid IndexError.        After drawing is over, centroid from previous part is #                removed from list by pop. So in next frame,centroids in this frame become initial points of line to draw.
    try:
            cv.Circle(imdraw,yellow[1],5,(0,255,255))
            cv.Line(imdraw,yellow[0],yellow[1],(0,255,255),3,8,0)
            yellow.pop(0)
            x=yellow[0][0]
            y=yellow[0][1]
            x=(x*1366/640)+10
            y=y*768/480
            x1=x
            y1=y
            #mouse.move(x,y)
            
    except IndexError:
            pass

   
    cv.Add(test,imdraw,test)


    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(keyboard,(0,0))
    
    
    screen.blit(yellowball,(x1-25,y1-25))
    pygame.display.update()
    char1=classify(x1,y1)
    if(char1!='.'):
        if(y==0):
            char2=char1
            stack.append(char2)
            y=y+1
            #print stack
        if(y>0) :
            char1=classify(x1,y1)
            if(char1!=char2):
                char2=char1
                y=y+1
                stack.append(char2)
                #print stack
                
        if(char1==' ' ): #and learn(stack)!=None
            y=0
            print stack
            str=''.join(stack)
            print str
            stack.pop[0]
            print d.suggest(str)
            del stack
            stack=list()
            
            """
            #do the machine learning operation here on the stack
            temp=learn(stack)
            print temp
            """
            
        
        
    
    
