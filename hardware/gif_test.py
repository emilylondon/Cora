from scipy.io.wavfile import read
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import time 
import queue 
import os 
import pigpio
from gpiozero import Button 
import threading

imgPath = "images/"
soundPath = "sounds/"

feelArr = ['sleeping.gif','happy.gif', 'sad.gif', 'mad.gif', 'worried.gif']
feelArrAud = ['intro.wav', 'happy.wav', 'sad.wav', 'mad.wav', 'worried.wav']
actionArr=['sleeping.gif','dance.gif', 'affirmations.gif', 'wiggle.gif', 'breathe.gif']
actionArrAud=['outro.wav','dance.wav', 'affirmations.wav', 'wiggle.wav', 'breathe.wav']

imageName=imgPath+feelArr[0]
soundName= soundPath + 'sleeping.mp3'
loc = 0
cnt =0
flg = 0
q = queue.Queue()
s = queue.Queue()
d = queue.Queue()

#GPIO button stuff/hardware 
leftButton = Button(16)
rightButton = Button(21)
selectButton = Button(20)

#GPIO LEDs 
RED_PIN   = 26
GREEN_PIN = 19
BLUE_PIN  = 13

#Initial color values 
RED=255
GREEN = 0
BLUE = 0 

#loc color array 
color=[[242,141,185], [255,255,0], [0,0,255], [255,0,0], [0,255,0]]

#Audio processing info 
samplerate=44100
resolution=20
spwin=samplerate/resolution

#Initialize the pi for pigpio
pi = pigpio.pi()

#helper functions 
def color_map(amp, color):
    mapped = color*(amp/9000)
    if mapped > 255:
        mapped = 255
    return mapped 

def window_rms(a, window_size=2):
    energy_list = []
    for s in range(0, a.shape[0], window_size):
        e = s + window_size
        energy = np.sqrt(np.mean(a[s:e]**2))
        energy_list.append(energy)
    return energy_list
def color_cycle():
    global RED
    global BLUE
    global GREEN
    global flg

    while flg!=0:
        for r in range(255):
            RED = r
            time.sleep(0.05)
        for b in range(255, 0, -1):
            BLUE = b
            time.sleep(0.05)
        for g in range(255):
            GREEN = g
            time.sleep(0.05)
        for r in range(255, 0, -1):
            RED = r 
            time.sleep(0.05)
        for b in range(255):
            BLUE = b
            time.sleep(0.05)
        for g in range(255, 0, -1):
            GREEN = g
            time.sleep(0.05)

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
            #im = im.zoom(2, 2)    
        frames = []
 
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
 
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
 
        if len(frames) == 1:
            self.config(image=next(self.frames))
            self.place(x=0, y=0)
        else:
            self.next_frame()
 
    def unload(self):
        self.config(image=None)
        self.frames = None
 
    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.place(x=0, y=0)
            self.after(self.delay, self.next_frame)
 
 #threads rip 
def iterate_through(loc):
    loc=0
    cnt=0
    flag=0
    global flg
    global RED
    global GREEN
    global BLUE
    RED=color[loc][0]
    GREEN=color[loc][1]
    BLUE=color[loc][2]
    print(RED)
    print(BLUE)
    print(GREEN)
    pi.set_PWM_dutycycle(RED_PIN, RED)
    pi.set_PWM_dutycycle(GREEN_PIN, GREEN)
    pi.set_PWM_dutycycle(BLUE_PIN, BLUE)
    while True:
        if leftButton.is_pressed:
            flg=0
            time.sleep(.005)
            if flag == 0: 
                s.put(soundPath + feelArrAud[0])
                flag = 1
            if (loc==1):
                loc=4
            else:
                loc-=1
            q.put(imgPath + feelArr[loc])
            s.put(soundPath + feelArrAud[loc])
            while leftButton.is_pressed:
                pass
        if rightButton.is_pressed:
            flg=0
            time.sleep(.005)
            if flag == 0: 
                s.put(soundPath + feelArrAud[0])
                flag = 1
            if (loc==4):
                loc=1
            else:
                loc+=1
            q.put(imgPath + feelArr[loc])
            s.put(soundPath + feelArrAud[loc])
            while rightButton.is_pressed:
                pass
        if selectButton.is_pressed:
            time.sleep(.005)
            while selectButton.is_pressed:
                print(cnt)
                if cnt==100:
                    loc=0
                    cnt=0
                    flag=0
                    flg=0
                cnt+=1 
                time.sleep(0.02)       
            
            q.put(imgPath + actionArr[loc])
            s.put(soundPath + actionArrAud[loc])
            if loc==1:
                flg=1
        time.sleep(0.02)

def play_audio():
    while True: 
        if (s.empty()!=True):
            audio = s.get()
            print(audio)
            os.system("omxplayer " + audio)
            a = read(audio)
            r = np.array(a[1], dtype=float)
            #2205 samples per window 
            psong=window_rms(r, window_size=int(spwin))
            d.put(psong)

def play_lights():
    while True:
        if (d.empty()!=True):
            psong=d.get()
            time.sleep(1)
            global RED
            global BLUE 
            global GREEN
        
            for t in range(len(psong)):
                r = color_map(psong[t], RED)
                g = color_map(psong[t], GREEN)
                b = color_map(psong[t], BLUE)
                pi.set_PWM_dutycycle(RED_PIN, r)
                pi.set_PWM_dutycycle(GREEN_PIN, g)
                pi.set_PWM_dutycycle(BLUE_PIN, b)
                time.sleep(0.05)
#demo :
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Cora')
    #root.attributes('-fullscreen', True)
    itTrd = threading.Thread(target=iterate_through, args=(loc,))
    audTrd = threading.Thread(target=play_audio)
    cycTrd = threading.Thread(target= color_cycle)
    lightTrd = threading.Thread(target= play_lights)
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(imageName)

    itTrd.start()
    audTrd.start()
    lightTrd.start()
    cycTrd.start()

    while True:
        if (q.empty()!=True):
            imageName=q.get()
            lbl.unload()
            lbl = ImageLabel(root)
            lbl.load(imageName)
        root.update()