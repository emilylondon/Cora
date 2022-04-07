from gpiozero import Button 

#GPIO button stuff/hardware 
leftButton = Button(20)
rightButton = Button(16)
selectButton = Button(21)


while True: 
    if leftButton.is_pressed:
        print("left!")
    if selectButton.is_pressed: 
        print("select!")
    if rightButton.is_pressed:
        print("right!")