import tkinter 
import sys 
from pynput import keyboard #sample inputs, will delete later
from PIL import Image, ImageTk
import time 

feelArr = ['happy.png', 'sad.png', 'angry.png', 'excited.png']
loc = 0

def showPIL(imageName):
    window = tkinter.Tk()

    #set attributes 
    #window.attributes('-fullscreen', True)
    window.title("Cora")

    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()

    #display image
    display = ImageTk.PhotoImage(imageName)
    
    label1 = tkinter.Label(image=display)
    label1.image = display

    label1.place(x=width/4,y=0)
    window.mainloop()

def on_press(key):
    try: 
        k = key.char
    except: 
        k = key.name
    if k == 'd':
        if loc!=3:
            loc = loc + 1
        else:
            loc = 0 
    elif k == 'a':
        if loc!=0:
            loc = loc - 1
        else: 
            loc = 3
    else:
        print("no in")
    loc = 0
    imageDisp = Image.open(feelArr[loc])
    showPIL(imageDisp)


if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    mainImage= Image.open("coraMain.png")
    showPIL(mainImage)

    while True:
        time.sleep(1)
