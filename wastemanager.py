import RPi.GPIO as GPIO
import tkinter as tk
import threading
from tkinter import ttk
import time
    
# Application Root
root = tk.Tk()
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for Passive Buzzer
BUZZER = 17
GPIO.setup(BUZZER, GPIO.OUT)

# Set up GPIO pins for Ultrasonic Distance Sensor
TRIGGER = 23
ECHO = 24
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set up GPIO pins for Buttons
RED_BUTTON = 5
BLUE_BUTTON = 6
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set up GPIO pins for LED Bar Graph
DATA = 16
CLK  = 18
GPIO.setup(DATA, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)

CmdMode  = 0x0000  # Work on 8-bit mode
ON       = 0x00ff  # 8-byte 1 data
SHUT     = 0x0000  # 8-byte 0 data

EMPTY = 10
FULL = 0.5
PASSCODE = ['R', 'B', 'B', 'R']
full_threshold = tk.StringVar(root)
percentage_var = tk.StringVar(root)
level = 0.5
is_locked = True
percentage = 40

# in real time, gets the distance from the sensor to the surface (bottom of container or waste) 
# and returns the current_level. Probably have a way in this function to check if the container
# is opened without being unlocked using is_unlocked.
def get_level():
    GPIO.output(TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
    time.sleep(0.00002)

    while GPIO.input(ECHO) == False:
        start_time = time.time()

    while GPIO.input(ECHO) == True:
        end_time = time.time()

    echo_duration = end_time - start_time

    distance = (echo_duration * 34300 / 2) - 2
    print(f"Distance: {distance} cm")

    return distance
    

def update_led_bar(percentage):
    num_leds = round(percentage / 10)  # assuming a 10-LED bar graph
    GPIO.output(DATA, CmdMode)
    for i in range(10):  # replace 8 with the number of LEDs on your bar graph
        if i < num_leds:
            # turn on LED
            GPIO.output(DATA, ON)
        else:
            # turn off LED
            GPIO.output(DATA, SHUT)
        # clock in the data
        GPIO.output(CLK, GPIO.HIGH)
        GPIO.output(CLK, GPIO.LOW)
    # latch the data
    GPIO.output(DATA, GPIO.LOW)
    GPIO.output(DATA, GPIO.HIGH)
    GPIO.output(DATA, GPIO.LOW)

# compares current_level to the provided threshold which 
# returns true if current_level goes over threshold. 
def is_full():
    global level
    global full_threshold
    if level > full_threshold:
        return True
    else:
        return False

# gets current_level and displays it on a GUI and on the LED screen 
# in real-time. Can simply use the LED Screen as a bar, like a battery level on a phone.
def get_percentage(distance):
    currentpercentage = (100 - (distance / EMPTY) * 100)
    return currentpercentage

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
def start_alarm(duration):
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER, GPIO.LOW)
    
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
            percentage = get_percentage(level)
            percentage_var.set(f'Current Waste Level: {percentage}%')
            update_led_bar(percentage)
            if is_locked and level > EMPTY:
                start_alarm(2)
            else:
                pass
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by the user.")
        GPIO.cleanup()

wasteLevelLabel = ttk.Label(root, textvariable=percentage_var)
wasteLevelLabel.grid(column=0, row=0)
thresholdEntry = ttk.Entry(root, textvariable=full_threshold)
thresholdEntry.grid(column=0, row=1)
setThresholdButton = ttk.Button(root, text='Set Threshold', command=set_threshold)
setThresholdButton.grid(column=0, row=2)

threading.Thread(target=main).start()

tk.mainloop()
