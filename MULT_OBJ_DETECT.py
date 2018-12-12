
import numpy as np
import cv2


# FILE FOR MULTIPLE OBJECT DETECTION ---------

def groups(mx,obj_breadth,not_present_range,fraction_to_present):
    obj_present=np.argwhere(mx>np.mean(mx)*fraction_to_present)
    a=[]
    i=1
    k=0
    obj_breadth=15
    while i<np.shape(obj_present)[0]:
        k=i
        while k<np.shape(obj_present)[0] and obj_present[k]-obj_present[k-1]==1:
            k=k+1
        if k-i>obj_breadth:
            a.append(int(obj_present[i-1]))  
            a.append(int(obj_present[k-1]))
            i=k
            i+=1
        else:
            i=k+not_present_range
        
    return(np.array(a))



#------------------all_tunable_params
obj_breadth=int(640*0.330)
l_h=0
l_s=13
l_v=0
h_h=200
h_s=36
h_v=255
not_present_range=int(640*0.20)
visibility=0.1
fraction_to_present=0.30
#---------------------------------------------------------------
cap=cv2.VideoCapture(0)

bar=np.zeros([10,600],np.uint8)

font=cv2.FONT_HERSHEY_SIMPLEX
#font=cv2.FONT_HERSHEY_SIMPLEX
#fou


while True:
    _,frame=cap.read()
    
    l_h=0
    l_s=13
    l_v=0
    h_h=200
    h_s=36
    h_v=255
    
    frame_pixels=480*640
    center=[240,320]
    
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    low_white=np.array([l_h,l_v,l_s])
    high_white=np.array([h_h,h_s,h_v])

    frame1=np.array(frame)
    frame2=np.array(frame)
    frame_final=np.array(frame)
    
    white_mask=cv2.inRange(hsv,low_white,high_white)
    white_mask_inv=cv2.bitwise_not(white_mask)
    
    foreground=cv2.bitwise_and(frame,frame1,mask=white_mask_inv)
    background=cv2.bitwise_and(frame,frame2,mask=white_mask)
    
    white_mask_inv[white_mask_inv==255]=1
    
    mx_tot=np.sum(white_mask_inv,axis=0)
   # my_tot=np.sum(white_mask_inv,axis=1)
    
    total=np.sum(mx_tot)
    
    
    a=groups(mx_tot,obj_breadth,not_present_range,fraction_to_present)
    i=0
    while i<np.shape(a)[0]-1:
        my=np.sum(white_mask_inv[:,a[i]:a[i+1]],axis=1)
        mx=mx_tot[a[i]:a[i+1]]
        x=np.arange(a[i],a[i+1])
        y=np.arange(np.shape(frame)[0])
        cx=int(np.sum(np.multiply((x+1),mx))/np.sum(mx))
        cy=int(np.sum(np.multiply((y+1),my))/np.sum(my))
        frame_final=cv2.circle(frame_final,(cx,cy),10,(0,0,255),-1)
        i+=2
    
    if total>visibility*frame_pixels:
        frame=frame_final
    else:
        frame=cv2.putText(frame,'Nothing present',(center[0]-100,center[1]-100),font,1,(0,255,0),1,cv2.LINE_AA)
    out.write(frame)
    cv2.imshow('original_feed',frame)
    cv2.imshow('background',background)
    cv2.imshow('foreground',foreground)
    #cv2.imshow('bar',bar)
    
    if cv2.waitKey(1)==27:
        break

cv2.destroyAllWindows()
cap.release()

