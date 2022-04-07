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

#prolonged button press 

def showPIL(imageName):
    #display image
    display = ImageTk.PhotoImage(imageName)
    
    label1 = tkinter.Label(image=display)
    label1.image = display

    label1.place(x=0,y=0)
  

#def clearWindow(frame):
        # destroy all widgets from frame
    #for widget in frame.winfo_children():
    #   widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    #frame.pack_forget()
    #frame.destroy()
    #frame = tkinter.Frame(window)


if __name__ == '__main__':
    window = tkinter.Tk()
    #set attributes 
    #window.attributes('-fullscreen', True)
    window.title("Cora")
    height = window.winfo_screenheight()


    mainImage= Image.open("coraMain.png")
    showPIL(mainImage)

    window.update()

    while True: 
        frame = tkinter.Frame(window) 
        if leftButton.is_pressed:
            if (loc == 0):
                loc=3
            else: 
                loc-=1
            print("left!")
            mainImage = Image.open(feelArr[loc])
            frame.destroy()
            frame=tkinter.Frame(window)
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
            frame.destroy()
            frame=tkinter.Frame(window)
            showPIL(mainImage)
        time.sleep(1)
        window.update()