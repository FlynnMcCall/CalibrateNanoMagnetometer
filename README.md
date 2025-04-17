# CalibrateNanoMagnetometer
Python script for calibrating the magnetic field sensor on my Arduino Nano 33 BLE.
This helps find bias in the sensors.

# Stuff to install
Make sure you have these python libraries installed.
```
$ pip install numpy
$ pip install matplotlib
$ pip install pyserial
```
Also install this arduino library: [Arduino_BMI270_BMM150](https://docs.arduino.cc/libraries/arduino_bmi270_bmm150/)

# What is this even supposed to do?
This is supposed to measure the bias in the sensors. Once you have the python script running and connected to the arduino, rotate the arduino in space to measure the earth's magnetic field. The circles plot the 3 axes against each other - in a perfect world, they would all be centred on 0.  
<img width="805" alt="Matplotlib output" src="https://github.com/user-attachments/assets/d744016d-b72f-4650-9da4-a6e12656ed3c" />

Try to create a definite perimeter all the way around the circles. Keep the arduino away from any magnets during this process.\\
We find the centre of the circles by taking the mean of the most extreme points along the two axes of the plots at various rotations. The final answer is just the mean of those measurements across the plots. 

<img width="813" alt="Final plot output" src="https://github.com/user-attachments/assets/945e9bd3-68be-4b11-9870-2fd1e9425281" />

Btw: You can generate a smoothed output by uncommenting lines 76-81 in the ino script, and commenting out the current output.

# How to use
- First set the serial port on line 6 of PlotMagnetometerBias.py.
- Write MagnetometerOutput.ino to the arduino.
- Close the IDE (so serial monitor is not in use).
- Run PlotMagnetometerBias.py
- You should now see 3 plots. Move your arduino around, try to complete the perimeter of the circles.
<img width="780" alt="PlotsB" src="https://github.com/user-attachments/assets/dec9b2ea-542f-4b47-808f-61c8f02585a6" />

- Keyboard interrupt the python program and enter the number of samples you want to use (recommended 10).
The script will print the bias of your sensors, and show the updated centres on your graph.

<img width="561" alt="Script output" src="https://github.com/user-attachments/assets/6f56da7a-4697-4f9d-b21b-a7880d417486" />
