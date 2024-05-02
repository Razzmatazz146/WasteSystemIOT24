import RPi.GPIO as GPIO
import time

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
is_unlocked = False

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

# Compares to a provided PASSCODE.
def code_check(button):
    global PASSCODE
    
    # Puts the initial button pressed into the input array
    input = [button]
    
    # Starts the timer
    start = time.monotonic()
    
    # For loop that expects the next 3 inputs
    for i in range(3):
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
        is_unlocked = True
        return

#that buzzes the alarm for as long as it is receiving true. 
def start_alarm():
    pass