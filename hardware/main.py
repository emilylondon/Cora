import tkinter 
import sys 
from gpiozero import Button 
from PIL import Image, ImageTk
import time 


feelArr = ['happy.png', 'sad.jpg', 'angry.png', 'excited.png']
loc = 0

#Button declarations 
leftButton = Button(20)
rightButton = Button(16)
selectButton = Button(21)


#prolonged button press 

#first instanse of image show, returns label to destroy latter
def initialShowPIL(imageName):
    display = ImageTk.PhotoImage(imageName)
    
    label1 = tkinter.Label(image=display)
    label1.image = display

    label1.place(x=0,y=0)
    return label1

#subsequent image shows, also returns label to destroy 
def showPIL(oldImage, imageName):

    #set attributes 
    #window.attributes('-fullscreen', True)
    oldImage.destroy()
    window.title("Cora")

    #display image
    display = ImageTk.PhotoImage(imageName)
    
    label1 = tkinter.Label(image=display)
    label1.image = display

    label1.place(x=0,y=0)
    return label1

if __name__ == '__main__':
    window = tkinter.Tk()
    #set attributes 
    #window.attributes('-fullscreen', True)
    window.title("Cora")
    height = window.winfo_screenheight()

    mainImage= Image.open("coraMain.png")
    oldImage=initialShowPIL(mainImage)

    window.update()

    while True: 
        frame = tkinter.Frame(window) 
        if count==5: #leftButton.is_pressed:
            count=0
            if (loc == 0):
                loc=3
            else: 
                loc-=1
            print("left!")
            mainImage = Image.open(feelArr[loc])
            oldImage=showPIL(oldImage, mainImage)
        if selectButton.is_pressed: 
            print("select!")
        if rightButton.is_pressed:
            if (loc == 3):
                loc = 0
            else:
               loc+=1
            print("right!")
            mainImage = Image.open(feelArr[loc])
            oldImage=showPIL(mainImage)
        time.sleep(1)
        window.update()