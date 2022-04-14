import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import time 
import queue 
from gpiozero import Button 
import threading

imgPath = "images/"
soundPath = "sounds/"

feelArr = ['happy.gif', 'sad.gif', 'mad.gif', 'worried.gif']
feelArrAud = ['happy.mp3', 'sad.mp3', 'mad.mp3', 'worried.mp3']
actionArr=['dance.gif', 'affirmations.gif', 'wiggle.gif', 'breathe.gif']
actionArrAud=['dance.mp3', 'affirmations.mp3', 'wiggle.mp3', 'breathe.mp3']

imageName=imgPath+'sleeping.gif'
soundName= soundPath + 'sleeping.mp3'
loc = 0
cnt =0
q = queue.Queue()

#GPIO button stuff/hardware 
leftButton = Button(16)
rightButton = Button(21)
selectButton = Button(20)

 
class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
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
    while True:
        if leftButton.is_pressed:
            if (loc==0):
                loc=3
            else:
                loc-=1
            q.put(imgPath + feelArr[loc])
            while leftButton.is_pressed
        if rightButton.is_pressed:
            if (loc==3):
                loc=0
            else:
                loc+=1
            q.put(imgPath + feelArr[loc])
            while rightButton.is_pressed
        if selectButton.is_pressed:
            q.put(imgPath + actionArr[loc])
        time.sleep(1)

#demo :
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Cora')
    #root.attributes('-fullscreen', True)
    itTrd = threading.Thread(target=iterate_through, args=(loc,))
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(imageName)

    itTrd.start()
    while True:
        if (q.empty()!=True):
            imageName=q.get()
            lbl.unload()
            lbl = ImageLabel(root)
            lbl.load(imageName)
        root.update()