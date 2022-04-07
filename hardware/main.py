import tkinter 
import sys 
from gpiozero import Button 
from PIL import Image, ImageTk
import time 


feelArr = ['happy.png', 'sad.jpg', 'angry.png', 'excited.png']
loc = 0

#button declarations 
leftButton = Button(20)
rightButton = Button(16)
selectButton = Button(21)

#initial images 
window = tkinter.Tk()
#set attributes 
#window.attributes('-fullscreen', True)
window.title("Cora")
height = window.winfo_screenheight()

mainImage= Image.open("coraMain.png")
display = ImageTk.PhotoImage(mainImage)
label1 = tkinter.Label(image=display)

label1.image = display
label1.place(x=0,y=0)

#prolonged button press 

def showPIL(imageName):
    #display image
    display = ImageTk.PhotoImage(imageName)
    
    label1 = tkinter.Label(image=display)
    label1.image = display

    label1.place(x=0,y=0)
  


if __name__ == '__main__':

    window.update()

    while True: 
        if leftButton.is_pressed:
            if (loc == 0):
                loc=3
            else: 
                loc-=1
            print("left!")
            mainImage = Image.open(feelArr[loc])
            label1.destroy()
            showPIL(mainImage)
        if selectButton.is_pressed: 
            print("select!")
        if rightButton.is_pressed:
            if (loc == 3):
                loc = 0
            else:
                loc+=1
            print("right!")
            mainImage = Image.open(feelArr[loc])
            showPIL(mainImage)
        window.update()