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

# How to use
- First set the serial port on line 6 of PlotMagnetometerBias.py.
- Write MagnetometerOutput.ino to the arduino.
- Close the IDE (so serial monitor is not in use).
- Run PlotMagnetometerBias.py
- You should now see 3 plots. Move your arduino around, try to fill in as much of the space as possible.
<img width="780" alt="PlotsA" src="https://github.com/user-attachments/assets/dec9b2ea-542f-4b47-808f-61c8f02585a6" />

- Keyboard interrupt the python program and enter the number of samples you want to use (recommended 10).
The script will print the bias of your sensors, and show the updated centres on your graph.

<img width="561" alt="Script output" src="https://github.com/user-attachments/assets/6f56da7a-4697-4f9d-b21b-a7880d417486" />
