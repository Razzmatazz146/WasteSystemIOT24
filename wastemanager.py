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
TRIGGER = 20
ECHO = 21
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Set up GPIO pins for Buttons
RED_BUTTON = 5
BLUE_BUTTON = 6
GPIO.setup(RED_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BLUE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

EMPTY = 10
FULL = 0.5
PASSCODE = ['R', 'B', 'B', 'R']
full_threshold = tk.StringVar(root)
percentage_var = tk.StringVar(root)
threshold = 100
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

# compares current_level to the provided threshold which 
# returns true if current_level goes over threshold. 
def is_full():
    global percentage
    global threshold
    if percentage > threshold:
        return True
    else:
        return False

# gets current_level and displays it on a GUI and on the LED screen 
# in real-time. Can simply use the LED Screen as a bar, like a battery level on a phone.
def get_percentage(distance):
    currentpercentage = (100 - (distance / EMPTY) * 100)
    return currentpercentage

def red_button_pressed():
    print("Red button pressed")
    return 'R'

def blue_button_pressed():
    if GPIO.input(BLUE_BUTTON) == GPIO.LOW:
        print("Blue button pressed")
        return 'B'

# Receives button inputs and compares it to the passcode. Unlocks if match.
def code_check():
    global PASSCODE
    global is_locked

    # Initialize the input array
    input = []

    while True:
        # Check if a button is pressed
        if GPIO.input(RED_BUTTON) == GPIO.LOW:
            print("Red button pressed")
            input.append('R')
            print(input)
            start = time.monotonic()  # Start the timer
        elif GPIO.input(BLUE_BUTTON) == GPIO.LOW:
            print("Blue button pressed")
            input.append('B')
            print(input)
            start = time.monotonic()  # Start the timer

        # If a button has been pressed
        if input:
            end = time.monotonic()
            
            # Timeout after 4 seconds and reset the array
            if end - start > 4:
                input = []
                print("Code timeout")
                time.sleep(1)
                continue

            # Check if the entered code is correct
            if input == PASSCODE:
                is_locked = False
                print("Correct! Unlocking.")
                input = []
                time.sleep(1)
                continue
                
            # Reset array if code is incorrect
            if len(input) > 3:
                input = []
                print("Incorrect")
                time.sleep(1)
                continue

        time.sleep(0.1)

#Func that buzzes the alarm for as long as it is receiving true. 
def start_alarm(duration):
    GPIO.output(BUZZER, GPIO.HIGH)
    print("BEEP")
    time.sleep(duration)
    GPIO.output(BUZZER, GPIO.LOW)
    
def set_threshold():
    global threshold
    try:
        threshold = float(full_threshold.get())
        if threshold > 100 or threshold < 0:
            raise ValueError
        else:
            print('New threshold: ', threshold, '%')
    except ValueError:
        print('Enter a number from 0 to 100')

def main():
    global threshold
    try:
        while True:
            level = get_level()
            percentage = get_percentage(level)
            rd_perc = round(percentage, 1)
            percentage_var.set(f'Current Waste Level: {rd_perc}%')
            print("Percentage:", rd_perc)
            print("Level:", level)
            if is_locked and level > EMPTY:
                percentage_var.set('CONTAINER OPEN!')
                start_alarm(2)
            elif percentage > threshold:
                percentage_var.set(f'Current Waste Level: FULL')
            elif not is_locked:
                percentage_var.set(f'CONTAINER UNLOCKED')
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
threading.Thread(target=code_check).start()

tk.mainloop()
