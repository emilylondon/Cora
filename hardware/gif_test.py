import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle
import time 
import queue 
import threading

path = "images/"
feelArr = ['happy.gif', 'sad.gif', 'mad.gif', 'worried.gif']
actionArr=['dance.gif', 'affirmations.gif', 'wiggle.gif', 'breathe.gif']
imageName=path+'sleeping.gif'
loc = 0
cnt =0
q = queue.Queue()

 
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
    cnt=0
    while True:
        print(cnt)
        if cnt==5: #leftButton.is_pressed:
            cnt=0
            if (loc == 0):
                loc=3
            else: 
                loc-=1
            q.put(path + feelArr[loc])
        cnt+=1
        time.sleep(1)

#demo :
if __name__ == '__main__':
    root = tk.Tk()
    root.title('Cora')
    root.attributes('-fullscreen', True)
    itTrd = threading.Thread(target=iterate_through, args=(loc,))
    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load(imageName)

    itTrd.start()
    while True:
        print("Hey")
        if (q.empty()!=True):
            imageName=q.get()
            lbl.unload()
            lbl = ImageLabel(root)
            lbl.load(imageName)
        
        print("please")
        print(imageName)
        root.update()