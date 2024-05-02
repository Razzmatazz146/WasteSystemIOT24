EMPTY = 0
FULL = 1
CODE = "R, B, B, R idk"

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

# that returns is_unlocked if provided sequence is correctly given within a 4 second span.
# Compares to a provided CODE.
def code_check():
 pass

#that buzzes the alarm for as long as it is receiving true. 
def start_alarm():
   pass