from scipy.io.wavfile import read

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import time 
import queue 
import os 
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
q = queue.Queue() # iamge
s = queue.Queue() # sound
d = queue.Queue() # 

#Initial screen width and height 
w=0
h=0

#GPIO button stuff/hardware 
leftButton = Button(16)
rightButton = Button(21)
selectButton = Button(20)


#loc color array 

#Audio processing info 
samplerate=44100
resolution=20
spwin=samplerate/resolution

#helper functions 
def image_scale(im):
    imgWidth, imgHeight = im.size
    ratio = min(w/imgWidth, h/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    im = im.resize((imgWidth,imgHeight))
    return im

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = image_scale(Image.open(im))
   
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

    while True:

        if leftButton.is_pressed:

            time.sleep(.005)
            if flag == 0: 
                s.put(soundPath + feelArrAud[0])
                flag = 1 
            if loc==0:
                loc=1
            elif (loc==1): 
                loc=4 
            else:
                loc-=1 

            q.put(imgPath + feelArr[loc])
            s.put(soundPath + feelArrAud[loc])

            while leftButton.is_pressed:
                pass
        if rightButton.is_pressed:

            time.sleep(.005)
            if flag == 0: 
                s.put(soundPath + feelArrAud[0])
                flag = 1
            if loc==0:
                loc=1                          
            elif (loc==4):
                loc=1
            else:
                loc+=1

            q.put(imgPath + feelArr[loc])
            s.put(soundPath + feelArrAud[loc])
       
            while rightButton.is_pressed:
                pass

        if selectButton.is_pressed:
            time.sleep(.005)
            if loc==0:
                loc=1
            while selectButton.is_pressed:
                print(cnt)
                if cnt==100:
                    loc=0
                    cnt=0
                    flag=0

                cnt+=1 
                time.sleep(0.02)       
            
            q.put(imgPath + actionArr[loc])
            s.put(soundPath + actionArrAud[loc])
            
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

#demo :
if __name__ == '__main__':
    #Initialize the pi for pigpio
    root = tk.Tk()
    root.title('Cora')
    #root.attributes('-fullscreen', True)
    w= root.winfo_screenwidth()
    h= root.winfo_screenheight()
    itTrd = threading.Thread(target=iterate_through, args=(loc,))
    audTrd = threading.Thread(target=play_audio)
    
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(imageName)

    itTrd.start()
    audTrd.start()
    

    while True:
        if (q.empty()!=True):
            imageName=q.get()
            lbl.unload()
            lbl = ImageLabel(root)
            lbl.load(imageName)
        root.update()