import time
import sys
from appJar import gui
# appJar can be found here, it is a great library for basic GUIs
# http://appjar.info/

import threading
from playsound import playsound


stop_threads = False

windowTimer = gui("Timer Basic Window", "1100x600")

def press(button):
    global stop_threads
    if button == "Abort":
        windowTimer.stop()
        stop_threads = True
    else:
        hou = windowTimer.getEntry("Hours")
        min = windowTimer.getEntry("Minutes")
        sec = windowTimer.getEntry("Seconds")
        print("hours:", hou, "minutes:", min, "seconds", sec)
        thread = threading.Thread(target=runTimer, args=(hou, min, sec))
        thread.start()


def runTimer(hou, min, sec):
    seconds = 0
    minutes = 0
    hours = 0
    runTimer = True
    hou = int(hou)
    sec = int(sec)
    min = int(min)
    if(sec >= 60):
        amount = 0
        amount += int(sec / 60)
        min += amount
        sec = sec - (amount * 60)
    if (min >= 60):
        amount = 0
        amount += int(min / 60)
        hou += amount
        min = min - (min * 60)

    timeInput = [hou, min, sec]

    current = time.time()

    while runTimer:
        global stop_threads
        if stop_threads:
            break
        #sys.stdout.write("\r{hours} Hours {minutes} Minutes {seconds} Seconds".format(hours=hours, minutes=minutes, seconds=seconds))
        #sys.stdout.flush()
        ongoingTime = ""
        ongoingTime += str(hours)
        ongoingTime += " "
        ongoingTime += str(minutes)
        ongoingTime += " "
        ongoingTime += str(seconds)
        ongoingTime += " "


        windowTimer.setMessage("Report", ongoingTime)

        time.sleep(1)
        seconds = int(time.time() - current) - minutes * 60 - hours * 60 * 60
        if seconds >= 60:
            minutes += 1
            seconds = 0
        if minutes >= 60:
            hours += 1
            minutes = 0


        #print(" time is", timeInput[0], timeInput[1], timeInput[2], " and count:", hours, minutes, seconds)

        if int(hours) == int(timeInput[0]) and int(minutes) == int(timeInput[1]) and int(seconds) == int(timeInput[2]):
            windowTimer.setMessage("Report", "!!!TIME PASSED!!!")
            playsound('EER.mp3')
            runTimer = False


if __name__ == '__main__':
    print("starting . . . ")
    #print("Plese enter the time you wish as hours minutes seconds")

    windowTimer.addLabel("title", "This is a basic Timer")
    windowTimer.setLabelBg("title", "gray")
    windowTimer.addLabelEntry("Hours")
    windowTimer.setEntry("Hours", "0")
    windowTimer.addLabelEntry("Minutes")
    windowTimer.setEntry("Minutes", "0")
    windowTimer.addLabelEntry("Seconds")
    windowTimer.setEntry("Seconds", "0")
    windowTimer.addButtons(["Accept", "Abort"], press)
    windowTimer.addMessage("Report", """The time will be shown here""")
    windowTimer.setMessageWidth("Report", 400)

    windowTimer.setFont(20)
    windowTimer.go()


