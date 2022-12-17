import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time

window_name = "Live Video"
check = True

def run(url, timePlay):
    mixer.init()
    # sound = mixer.Sound('alarm.wav')
    # sound = mixer.Sound('source/music/rockabye.wav')
    sound = mixer.Sound(url)

    face = cv2.CascadeClassifier('haar cascade files\haarcascade_frontalface_alt.xml')
    leye = cv2.CascadeClassifier('haar cascade files\haarcascade_lefteye_2splits.xml')
    reye = cv2.CascadeClassifier('haar cascade files\haarcascade_righteye_2splits.xml')


    # python -m PyQt5.uic.pyuic -x untitled.ui -o main_layout.py
    lbl=['Close','Open']

    model = load_model('models/cnn.h5')
    path = os.getcwd()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    cv2.namedWindow(window_name)
    if cap.isOpened():
        flag, frame = cap.read()
    thicc=2
    rpred=[99]
    lpred=[99]
    count=0
    score=0
    while(check):
        ret, frame = cap.read()
        
        height,width = frame.shape[:2]
       
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
        left_eye = leye.detectMultiScale(gray)
        right_eye =  reye.detectMultiScale(gray)

        cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

        for (x,y,w,h) in right_eye:
            r_eye=frame[y:y+h,x:x+w]
            count=count+1
            r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
            r_eye = cv2.resize(r_eye,(24,24))
            r_eye= r_eye/255
            r_eye=  r_eye.reshape(24,24,-1)
            r_eye = np.expand_dims(r_eye,axis=0)
            rpred = np.argmax(model.predict(r_eye), axis=-1)

            if rpred.all()==1:
                lbl='Open' 
            if rpred.all()==0:
                lbl='Closed'
            break

        for (x,y,w,h) in left_eye:
            l_eye=frame[y:y+h,x:x+w]
            count=count+1
            l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
            l_eye = cv2.resize(l_eye,(24,24))
            l_eye= l_eye/255
            l_eye=l_eye.reshape(24,24,-1)
            l_eye = np.expand_dims(l_eye,axis=0)
            
            lpred = (model.predict(l_eye) > 0.5).astype("int32")
            
            if lpred.all()==1:
                lbl='Open'   
            if lpred.all()==0:
                lbl='Closed'
            break

        if np.logical_and((rpred.all()) == 0, (lpred.all()) == 0):
            score= score+1
            cv2.putText(frame,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        
        else:
            score=score-1
            cv2.putText(frame,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        
            
        if(score<0):
            score=0   
        cv2.putText(frame,'Score:'+str(score),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
        if(score>15):
            score=0
            #person is feeling sleepy so we beep the alarm
            cv2.imwrite(os.path.join(path,'image.jpg'),frame)
            try:
                timeMax = int(sound.get_length())*1000
                if(timePlay >= timeMax):
                    timePlay = timeMax
                mixer.Sound.play(sound, 0, timePlay, 1000)
                # sound.play()
                
            except:  # isplaying = False
                pass
            if(thicc<16):
                thicc= thicc+2
            else:
                thicc=thicc-2
                if(thicc<2):
                    thicc=2
            cv2.rectangle(frame,(0,0),(width,height),(0,0,255),thicc)
            
            if cv2.waitKey(timePlay) & 0xFF == ord('q'):
                break
        else:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.imshow(window_name,frame)

def stopCamera():
    check =  False
    # cv2.destroyWindow(window_name)
    # cap.release()
    cv2.destroyAllWindows()

