#**************************************************************************************************************
#*************************************importing****************************************************************
#**************************************************************************************************************






import numpy as np
import cv2
import math
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS
from gpiozero import Button
import serial
import time



#**************************************************************************************************************
#*************************************setup****************************************************************
#**************************************************************************************************************

cap = cv2.VideoCapture(0)
serialcom=serial.Serial('/dev/ttyACM0',9600)
button =Button(21)
velocity=0
anglefinale=0
velocity=0
positionfinale=0
output=anglefinale,velocity,positionfinale
output=str(output)
serialcom.write(output.encode())



#**************************************************************************************************************
#*************************************define view function****************************************************************
#**************************************************************************************************************
def speak(text):#song function
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception: " + str(e))

    return said



   
    
#**************************************************************************************************************
#*************************************song parte****************************************************************
#**************************************************************************************************************
while True:
    if button.is_pressed:#button of rasberry pi

        text = get_audio()

        if "go" in text:
            speak("ok")
            velocity=1
        elif "slow" in text:
            speak("ok")
            velocity = 2
        elif "fast" in text:
            speak("ok i am going fast")
            velocity = 3

        elif "hello" in text:
            speak("hi sir")
        serialcom.write(output.encode())
        velocity=1


    else:
       while(True):
        lista=[]
        
        linefinale=[]
        ret, frame = cap.read()
        
        imc=frame[340:480,45:635]
        edges=cv2.Canny(imc,100,150)

        lines = cv2.HoughLinesP(edges,1,np.pi/180,50,maxLineGap=200)
        lin=0
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                longeur=math.sqrt(((x1-x2)**2)+((y1-y2)**2))
                angle=math.atan(((y2-y1)/(x2-x1)))
                p=((x1+((x2-x1)/2)),(y1+((y2-y1)/2)))
                if p[0]<200:
                    k=0
                else:
                    k=1
                lista.append((longeur,angle,p,lin,k))
                lin+=1
        lista=sorted(lista, reverse=True,key=lambda x: x[0])
        if len(lista)>0:
           if len(linefinale)<1:
                
                linefinale.append(lista[0])
                for element in range(len(lista)):
                    if linefinale[0][4]!=lista[element][4]:
                        linefinale.append(lista[element])
                        break
        
      
        if len(linefinale)>1:
            x1d=lines[linefinale[0][3]][0][0]
            x2d=lines[linefinale[0][3]][0][1]
            y1d=lines[linefinale[0][3]][0][2]
            y2d=lines[linefinale[0][3]][0][3]
            x1g=lines[linefinale[1][3]][0][0]
            x2g=lines[linefinale[1][3]][0][1]
            y1g=lines[linefinale[1][3]][0][2]
            y2g=lines[linefinale[1][3]][0][3]
            anglefinale=(linefinale[0][1]+linefinale[1][1])/2
            
            anglefinale = round(math.degrees(anglefinale))
            positionfinale = (linefinale[0][2][0] + linefinale[1][2][0]) / 2
            cv2.line(imc,(x1d,x2d),(y1d,y2d),(0,255,0),5)
            cv2.line(imc,(x1g,x2g),(y1g,y2g),(0,255,0),5)
            positionfinale=round(positionfinale)
            output=anglefinale,velocity,positionfinale
            output=str(output)+"\n"
            serialcom.write(output.encode())
            print(output)
        cv2.imshow('frame',frame)
        cv2.imshow('edges',edges)
        cv2.imshow('imc',imc)
        cv2.waitKey(1)
        if button.is_pressed:
            break
    cap.release
    cv2.destroyAllWindows()
