from gpiozero import Button 

def displayState(state):
    filename=feelArr[state]
    #display filename on screen

def doState(state):
    if state==0:
        playHappy()
    elif state==1:
        playSad()
    elif state==2:
        playWorried()
    else:
        playMad()

def playHappy():
    print("playing happy!")
    #do happy action

def playSad():
    print("playing sad!")
    #do sad action

def playWorried():
    print("playing worried!")
    #do worried action

def playMad():
    print("playing mad!")
    #do mad action


#GPIO button stuff/hardware 
leftButton = Button(20)
rightButton = Button(16)
selectButton = Button(21)

"""
0 - happy
1 - sad
2 - worried
3 - mad
4 - sleep
"""

feelArr = ['happy.png', 'sad.png', 'worried.png', 'mad.png', 'sleep.png']
leftMap={4:1, 0:3, 1:0, 2:1, 3:2}
rightMap={4:1, 0:1, 1:2, 2:3, 3:0}
stateMap={0:"happy", 1:"sad", 2:"worried", 3:"mad", 4:"sleep"}
state=4
reset=0
sleepCount=0

#show sleep
displayState(state)

while True: 

    if leftButton.is_pressed:
        state=leftMap[state]
        showState(state)
        print("left! to "+str(stateMap[state]))

    elif rightButton.is_pressed: 
        state=rightMap[state]
        showState(state)
        print("right! to "+str(stateMap[state]))

    elif selectButton.is_pressed:
        reset=0
        print("selected!"+str(stateMap[state]))
        if state==4:
            state=0
        else:
            doState(state)
    
    if reset==300:
        print("going back to sleep!")
        state=0
        displayState(state)
    reset+=1

    time.sleep(0.2)

