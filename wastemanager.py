# import RPi.GPIO as GPIO
import tkinter as tk
import threading
from tkinter import ttk
import time

class GPIO:
    OUT = 0
    IN = 0
    PUD_UP = 0
    def setup(a, b, *args, **kwargs):
        return
    
# Application Root
root = tk.Tk()

# Set up GPIO pins for Passive Buzzer
BUZZER = 17
GPIO.setup(BUZZER, GPIO.OUT)

# Set up GPIO pins for Ultrasonic Distance Sensor
TRIGGER = 23
ECHO = 24
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set up GPIO pins for Buttons
BUTTON1 = 5
BUTTON2 = 6
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up GPIO pins for LED Bar Graph
DATA = 16
CLK  = 18
GPIO.setup(DATA, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)

CmdMode  = 0x0000  # Work on 8-bit mode
ON       = 0x00ff  # 8-byte 1 data
SHUT     = 0x0000  # 8-byte 0 data

EMPTY = 0
FULL = 1
PASSCODE = ['R', 'B', 'B', 'R']
full_threshold = tk.StringVar(root)
level = 0.5
is_locked = True

# in real time, gets the distance from the sensor to the surface (bottom of container or waste) 
# and returns the current_level. Probably have a way in this function to check if the container
# is opened without being unlocked using is_unlocked.
def get_level():
    pass

# compares current_level to the provided threshold which 
# returns true if current_level goes over threshold. 
def is_full(threshold):
    pass

# gets current_level and displays it on a GUI and on the LED screen 
# in real-time. Can simply use the LED Screen as a bar, like a battery level on a phone.
def update_visuals(current_level):
    pass

# Receives button inputs and compares it to the passcode. Unlocks if match.
def code_check(button):
    global PASSCODE
    global is_locked
    
    # Puts the initial button pressed into the input array
    input = [button]
    
    # Starts the timer
    start = time.monotonic()
    
    # For loop that expects the next 3 inputs
    for i in range(len(PASSCODE)-1):
        if 'red button':
            input.append('R')
        elif 'blue button':
            input.append('B')
    
    # Stops the timer
    end = time.monotonic()
    
    # Checks if time elapsed is greater than 4 seconds
    if end - start > 4:
        return
    elif input != PASSCODE:
        return
    else:
        is_locked = False
        return

#that buzzes the alarm for as long as it is receiving true. 
def start_alarm():
    pass

def set_threshold():
    try:
        threshold = float(full_threshold.get())
        if threshold > 100 or threshold < 0:
            raise ValueError
        else:
            print('New threshold: ', threshold, '%')
    except ValueError:
        print('Enter a number from 0 to 100')

def main():
    try:
        while True:
            level = get_level()
            if is_locked and level < EMPTY:
                start_alarm()
            else:
                update_visuals()
    except Exception:
        print(Exception)
    finally:
        GPIO.cleanup()

wasteLevelLabel = ttk.Label(root, text='Current Waste Level: 0%')
wasteLevelLabel.grid(column=0, row=0)
thresholdEntry = ttk.Entry(root, textvariable=full_threshold)
thresholdEntry.grid(column=0, row=1)
setThresholdButton = ttk.Button(root, text='Set Threshold', command=set_threshold)
setThresholdButton.grid(column=0, row=2)

tk.mainloop()