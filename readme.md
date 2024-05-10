# SETUP

### Place HC-SR04 Hypersonic Sensor ~ 10 cm away from a surface you wish measured. 

*Distance is set to 10 by default for the **EMPTY** constant in the code.*

### Launch the script

# READING THE UI

Label at the top shows the current level of the container as a percentage. By default, the threshold is **100%**.

In the textbar, input a number from **0 - 100**, then click the **'Set Threshold'** button to set your desired threshold. 

*If the level goes over the threshold, the label will read as **'Current Waste Level: FULL'**.*

# UNLOCKING THE CONTAINER

### To unlock the container, simply provide the unlock code using the red and blue buttons. 

## By default, the code is "RED, BLUE, BLUE, RED"

If unsuccessful, it will simply reset and you can try again. 

If successful, the label will read as **'CONTAINER UNLOCKED'**

*If container is opened before unlocking, the alarm will ring and the label will read as **'CONTAINER OPEN!'**.*
