#!/usr/bin/env python

# Source https://thisisyetanotherblog.wordpress.com/2016/09/14/raspberry-pi-3-wears-a-display-o-tron-hat/

print('''
Switch between different views using the Display-o-Tron HAT buttons
 
Main button: Display date and time
Right: Display number of unread emails
Left: Display system statistics
Down: Display process status
Up: TODO find something else to display
 
Press CTRL+C to exit.
''')
 
import dothat.touch as touch
import dothat.lcd as lcd
import dothat.backlight as backlight
import signal
import sys
 
import psutil
import urllib2
import subprocess
import imaplib
import time
from datetime import date
import calendar
import threading
 
'''
 
Captouch provides the @captouch.on() decorator
to make it super easy to attach handlers to each button.
 
The handler will receive 'channel'( corresponding to a particular
button ID ) and 'event' ( corresponding to press/release ) arguments.
'''
 
'''DISPLAY utilities'''
# store time of last button touch
# to be able to reset backlight LEDs
oldTime = time.time()
turnedOff = True
 
def resetBacklightLEDs():
    global oldTime
    oldTime = time.time()
    global turnedOff
    turnedOff = False
 
def clearDOT():
    lcd.clear()
 
def colorDOT(r, g, b):
    backlight.rgb(r, g, b)
 
def turnOnLEDsDOT():
    # turn on LEDs one by one in a row
    for led in range(6):
        backlight.graph_set_led_state(led, 1)
        time.sleep(0.1)
    pass
 
def turnOffDOT():
    colorDOT(0, 0, 0)  # backlight off
    backlight.off()
    backlight.graph_off()  # side LEDs off
    global turnedOff
    turnedOff = True
 
def dotClock():
    clearDOT()
 
    d = time.strftime("%d.%m.%Y")
    t = time.strftime("%H:%M")
    the_date = date.today()
    day = calendar.day_name[the_date.weekday()]
    print day + ", " + d + " / " + t
 
    lcd.set_cursor_position(3, 0)
    lcd.write(day)
    lcd.set_cursor_position(3, 1)
    lcd.write(d)
    lcd.set_cursor_position(5, 2)
    lcd.write(t)
 
def dotMails(login, password):
    nofUnreadEmails = check_googlemail(login, password)
    if nofUnreadEmails > 0:
        lcd.write("Unread Emails: " + str(nofUnreadEmails))
        showNewMessages(200, 0, 0)
 
    else:
        lcd.write("No new mail")
 
def dotSystemStats():
    lcd.set_cursor_position(0, 0)
    lcd.write(check_internet())
 
    lcd.set_cursor_position(0, 1)
    lcd.write("CPU: " + check_CPU())
 
    lcd.set_cursor_position(0, 2)
    lcd.write("Memory: " + check_memory())
 
def check_internet():
    try:
        # ping google to check whether internet connection works
        response = urllib2.urlopen('http://www.google.com', timeout=1)
        return "Internet: OK"
    except urllib2.URLError as err: pass
    return "Internet connection broken"
 
def check_CPU():
    cpu_usage = str(psutil.cpu_percent(interval=None)) + " %"
    print "CPU usage: " + cpu_usage
    return cpu_usage
 
def check_memory():
    mem = psutil.virtual_memory()
    # print "Memory: " + str(mem)
    memory_used = str(mem.percent) + " %"
    print "Memory used: " + memory_used
    THRESHOLD = 100 * 1024 * 1024  # 100MB
    if mem.available >= THRESHOLD:
        print("Warning, memory low")
        return "Warning, memory low"
    return memory_used
 
def get_pid(name):
    try:
        pids = subprocess.check_output(["pidof", name])
    except subprocess.CalledProcessError as pids:
        print "error code", pids.returncode, pids.output
        return ""
    return map(int, pids.split())
 
def get_single_pid(name):
    return int(check_output(["pidof", "-s", name]))
 
def check_process(name):
    PID = get_pid(name)
    if len(PID) == 1:
        print "PID " + name + ": " + str(PID[0])
        p = psutil.Process(PID[0])
        status = ""
        if p.status == psutil.STATUS_ZOMBIE:
            status = "Process " + name + " died"
            print status
        else:
            status = "Process " + name + " OK"
            print status
            return status
        return ""
 
def dotProcessStats():
    lcd.set_cursor_position(0, 0)     
    process1 = check_process('geany')
    if len(process1) > 1 :    
        lcd.write(process1)
    else:
        lcd.write("geany is dead.")
 
    lcd.set_cursor_position(0, 1)
    process2 = check_process('bash')
    if len(process2) > 1 :
        lcd.write(process2)
    else:
        lcd.write("bash is dead.")
 
    lcd.set_cursor_position(0, 2)
    process3 = check_process('firefox')
    if len(process3) > 1 :
        lcd.write(process3)
    else:
        lcd.write("firefox is dead.")
 
def check_googlemail(login, password):
    # if new mail return # emails
    obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    obj.login(login, password)
    obj.select()
    nofUnreadMessages = len(obj.search(None, 'UnSeen')[1][0].split())
    print "Unread emails: " + str(nofUnreadMessages)
    return nofUnreadMessages
 
class ShowNewMessagesThread (threading.Thread):
    red, green, blue = 0, 0, 0  # static elements, it means, they belong to the class
 
    def run (self):
        colorDOT(self.red, self.green, self.blue)
        for i in range(0, 3):
            turnOnLEDsDOT()
            time.sleep(2)
            turnOffDOT()
            time.sleep(2)
 
            if i == 2:
                print "stop ShowNewMessagesThread"
                self.do_run = False  # stop thread
                break
 
snmt = ShowNewMessagesThread()
def showNewMessages(r, g, b):
    global snmt
    if snmt.is_alive():
        return
    snmt = ShowNewMessagesThread()
    snmt.red = r
    snmt.green = g
    snmt.blue = b
    snmt.daemon = True  # enable stop of thread along script with Ctrl+C
    snmt.start()
 
class AlightThread (threading.Thread):
    red, green, blue = 0, 0, 0  # static elements, it means, they belong to the class
 
    def run (self):
        colorDOT(self.red, self.green, self.blue)
        while True:
            if turnedOff == False:
                if time.time() - oldTime > 5:
                    print "stop AlightThread"
                    turnOffDOT()
                    self.do_run = False  # stop thread
                    break
 
at = AlightThread()
def alightDisplay(r, g, b):
    global at
    if at.is_alive():
        return
    at = AlightThread()
    at.red = r
    at.green = g
    at.blue = b
    at.daemon = True  # enable stop of thread along script with Ctrl+C
    at.start()
 
class ClockThread (threading.Thread):
    def run (self):
        print "run update clock thread " + str(self)
        dotClock()
        self.do_run = False  # stop thread
 
    def stopClockThread(self):
        self.do_run = False  # stop thread
 
ct = ClockThread()
def updateClock():
    global ct
    if ct.is_alive():
        print "Clock thread " + str(ct) + " is alive."
        ct.stopClockThread()
        return
    print "Launching clock thread " + str(ct)
    ct = ClockThread()
    ct.daemon = True  # enable stop of thread along script with Ctrl+C
    ct.start()
 
'''DOT touch button handler'''
@touch.on(touch.UP)
def handle_up(ch, evt):
    print("Up pressed: TODO find another useful display idea")
    clearDOT()
    alightDisplay(255, 0, 255)
    lcd.write("Up up and away: TODO")
    resetBacklightLEDs()
 
@touch.on(touch.DOWN)
def handle_down(ch, evt):
    print("Down pressed: display process states")
    clearDOT()
    alightDisplay(255, 0, 0)
    dotProcessStats()
    resetBacklightLEDs()
 
@touch.on(touch.LEFT)
def handle_left(ch, evt):
    print("Left pressed: display system statistics")
    clearDOT()
    alightDisplay(0, 100, 200)
    dotSystemStats()
    resetBacklightLEDs()
 
@touch.on(touch.RIGHT)
def handle_right(ch, evt):
    print("Right pressed, check for new email")
    clearDOT()
    alightDisplay(100, 200, 255)
    dotMails('email adress', 'password')
    resetBacklightLEDs()
 
@touch.on(touch.BUTTON)
def handle_button(ch, evt):
    print("Main button pressed: show date and time")
    clearDOT()
    alightDisplay(255, 255, 255)
    updateClock()
    resetBacklightLEDs()
 
@touch.on(touch.CANCEL)
def handle_cancel(ch, evt):
    print("Cancel pressed!")
    clearDOT()
    backlight.rgb(0, 0, 0)
    lcd.write("Cancel")
    resetBacklightLEDs()
    alightDisplay(20, 20, 20)
 
'''main'''
if __name__ == '__main__':
    try:
        while True:
            timeDiff = time.time() - oldTime
            # print "time diff: " + str(timeDiff)
    
            # update clock every minute
            if timeDiff > 59 or timeDiff < 0.5:
                oldTime = time.time()
                alightDisplay(255, 255, 255)
                updateClock()
                time.sleep(1)
            except KeyboardInterrupt:
                print "exit"
                clearDOT()
                turnOffDOT()
                sys.exit()