import numpy as np 
import cv2

import serial
ser=serial.Serial('/dev/ttyACM0',9600)

#ls -l /dev/ttyACM*
#sudo chmod a+rw /dev/dev/ttyACM0 

def reverse(xx):
    k=''
    for x in range(len(xx)):
        k=k+xx[len(xx)-x-1]
    return k

import numpy as np 
import cv2

#
cap=cv2.VideoCapture(0)
visibility=0.05

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)


l_h=0
l_s=13
l_v=0
h_h=200
h_s=36
h_v=255
z=500
font=cv2.FONT_HERSHEY_SIMPLEX

#def nothing(x):
#    pass
#
#
#cv2.createTrackbar('l_h','bar',0,20,nothing)
#cv2.createTrackbar('l_s','bar',0,50,nothing)
#cv2.createTrackbar('l_v','bar',0,150,nothing)
#cv2.createTrackbar('h_h','bar',0,100,nothing)
#cv2.createTrackbar('h_s','bar',0,150,nothing)
#cv2.createTrackbar('h_v','bar',200,255,nothing)
#cv2.createTrackbar('a','bar',0,240,nothing)
#cv2.createTrackbar('b','bar',241,480,nothing)
#cv2.createTrackbar('c','bar',0,320,nothing)
#cv2.createTrackbar('d','bar',324,640,nothing)


while True:
    _,frame=cap.read()
    
    #a=cv2.getTrackbarPos('a','bar')
    #b=cv2.getTrackbarPos('b','bar')
    #c=cv2.getTrackbarPos('c','bar')
    #d=cv2.getTrackbarPos('d','bar')
    

    
    frame_pixels=480*640
    center=[240,320]
    
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    
    #l_h=cv2.getTrackbarPos('l_h','bar')
    #h_h=cv2.getTrackbarPos('h_h','bar')
    #
    #l_s=cv2.getTrackbarPos('l_s','bar')
    #h_s=cv2.getTrackbarPos('h_s','bar')
    #
    #l_v=cv2.getTrackbarPos('l_v','bar')
    #h_v=cv2.getTrackbarPos('h_v','bar')
    
    
    low_white=np.array([l_h,l_v,l_s])
    high_white=np.array([h_h,h_s,h_v])

    frame1=np.array(frame)
    frame2=np.array(frame)
    
    white_mask=cv2.inRange(hsv,low_white,high_white)
    white_mask_inv=cv2.bitwise_not(white_mask)
    
    foreground=cv2.bitwise_and(frame,frame1,mask=white_mask_inv)
    background=cv2.bitwise_and(frame,frame2,mask=white_mask)
    
    white_mask_inv[white_mask_inv==255]=1
    
    mx=np.sum(white_mask_inv,axis=0)
    my=np.sum(white_mask_inv,axis=1)
    
    total=np.sum(mx)
    
    x=np.arange(np.shape(frame)[1])
    y=np.arange(np.shape(frame)[0])
    
    if total>visibility*frame_pixels:
        cx=int(np.sum(np.multiply((x+1),mx))/np.sum(mx))
        cy=int(np.sum(np.multiply((y+1),my))/np.sum(my))
        frame=cv2.circle(frame,(cx,cy),10,(0,0,255),-1)
        angle_x=str(int(np.arctan((320-cx)*0.000756)*180/3.14)+90)
        angle_y=str(int(np.arctan((cy-240)*0.000808)*180/3.14)+90)
        angle_x=reverse(angle_x)
        angle_y=reverse(angle_y)
        
        ret_value=angle_x+'/'+angle_y+'/'
        for k in ret_value:
            ser.write(k.encode())
        
        
        
    else:
        frame=cv2.putText(frame,'Nothing present',(center[0]-100,center[1]-100),font,1,(0,255,0),1,cv2.LINE_AA)
        ret_value=None
    

        
    
    frame=cv2.circle(frame,(center[1],center[0]),10,(255,0,0),-1)
    
    cv2.imshow('original_feed',frame)
    cv2.imshow('background',background)
    cv2.imshow('foreground',foreground)
    #cv2.imshow('bar',bar)
    print(ret_value)
 
    
    if cv2.waitKey(1)==27:
        break

cv2.destroyAllWindows()
cap.release()

