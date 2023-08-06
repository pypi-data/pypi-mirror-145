#Laksh Patel ©2022

import time

from pynput.keyboard import Controller

keyboard = Controller()

def typewrite(string,timeint, countdown):
    time.sleep(countdown)
    r = string
    time.sleep(timeint)
    y = 0
    keyboard.type(r[0])
    r = string[1:]
    for i in range(0, int(len(r)), 1):
        r = string[1:]
        keyboard.type(r[y])
        y = y + 1
        time.sleep(timeint)

def type(string, countdown):
    time.sleep(countdown)
    stringnew = string
    e = 0
    keyboard.type(stringnew[0])
    stringnew = string[1:]
    for i in range(0, int(len(stringnew)), 1):
        stringnew = string[1:]
        keyboard.type(stringnew[e])
        e = e + 1

