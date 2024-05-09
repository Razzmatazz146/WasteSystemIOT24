# Set up GPIO pins for LED Bar Graph
DATA_Pin = 23
CLK_Pin  = 24

CmdMode  = 0x0000  # Work on 8-bit mode
ON       = 0x00ff  # 8-byte 1 data
SHUT     = 0x0000  # 8-byte 0 data

global s_clk_flag
s_clk_flag = 0

def send16bitData(data):
	global s_clk_flag
	for i in range(0, 16):
		if data & 0x8000:
			GPIO.output(DATA_Pin, GPIO.HIGH)
		else:
			GPIO.output(DATA_Pin, GPIO.LOW)
		
		if s_clk_flag == True:
			GPIO.output(CLK_Pin, GPIO.LOW)
			s_clk_flag = 0
		else:
			GPIO.output(CLK_Pin, GPIO.HIGH)
			s_clk_flag = 1
		time.sleep(0.001)
		data = data << 1

def latchData():
	latch_flag = 0
	GPIO.output(DATA_Pin, GPIO.LOW)
	
	time.sleep(0.05)
	for i in range(0, 8):
		if latch_flag == True:
			GPIO.output(DATA_Pin, GPIO.LOW)
			latch_flag = 0
		else:
			GPIO.output(DATA_Pin, GPIO.HIGH)
			latch_flag = 1
	time.sleep(0.05)
  
def sendLED(LEDstate):
    for i in range(0, 12):
        if (LEDstate & 0x0001) == True:
            print(LEDstate)
            send16bitData(ON)
        else:
            send16bitData(SHUT)
            LEDstate = LEDstate >> 1

def setup():

	GPIO.setwarnings(False)
	#GPIO.setmode(GPIO.BOARD)

	GPIO.setup(DATA_Pin, GPIO.OUT)
	GPIO.setup(CLK_Pin,  GPIO.OUT)

	GPIO.output(DATA_Pin, GPIO.LOW)
	GPIO.output(CLK_Pin,  GPIO.LOW)
    
def led_data():
    global i
    while True:
        print(i)
        send16bitData(CmdMode)
        sendLED(i)
        latchData()
        time.sleep(0.1)
    
def update_led(percentage):
    global i
    # Calculate the number of LEDs to light up
    num_leds = int(percentage / 10)

    # Ensure the number of LEDs is between 0 and 10
    num_leds = max(0, min(num_leds, 10))

    # Calculate the value to send to the LEDs
    i = (1 << num_leds) - 1
