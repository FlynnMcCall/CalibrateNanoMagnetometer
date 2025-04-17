import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

ser = serial.Serial('/dev/cu.usbmodem101', 9600)

# Initialize plot
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(6, 6))
x_data, y_data, z_data = [], [], []

ax1.scatter(x_data, y_data)
ax2.scatter(y_data, z_data)
ax3.scatter(z_data, x_data)
ax1.set_title("x y")
ax2.set_title("y z")
ax3.set_title("z x")

maxx = 0
maxy = 0
maxz = 0
minx = 0
miny = 0
minz = 0
centx = np.array([0])
centy = np.array([0])
centz = np.array([0])
numSamples = 0

def getNewInput():
    global maxx, maxy, maxz, minx, miny, minz
    line = ser.readline().decode('utf-8').rstrip()
    data_array = np.fromstring(line, sep=',').astype(float)
    if data_array.shape[0] == 3:
        x_data.append(data_array[0])
        y_data.append(data_array[1])
        z_data.append(data_array[2])

        maxx = max(data_array[0], maxx)
        maxy = max(data_array[1], maxy)
        maxz = max(data_array[2], maxz)
        minx = min(data_array[0], minx)
        miny = min(data_array[1], miny)
        minz = min(data_array[2], minz)
        centx[0] = (maxx + minx) / 2
        centy[0] = (maxy + miny) / 2
        centz[0] = (maxz + minz) / 2

def redrawGraphs():
    ax1.clear()  # clearing the axes
    ax2.clear()
    ax3.clear()
    ax1.scatter(x_data,y_data, s=20, c = 'b', alpha = 0.2)  # creating new scatter chart with updated data
    ax2.scatter(y_data,z_data, s=20, c = 'r', alpha = 0.2)
    ax3.scatter(z_data,x_data, s=20, c = 'g', alpha = 0.2)

    ax1.grid(True)
    ax1.set_xlim(-100, 100)
    ax1.set_ylim(-100,100)
    ax1.set_aspect('equal', 'box')

    ax2.grid(True)
    ax2.set_xlim(-100, 100)
    ax2.set_ylim(-100,100)
    ax2.set_aspect('equal', 'box')

    ax3.grid(True)
    ax3.set_xlim(-100, 100)
    ax3.set_ylim(-100,100)
    ax3.set_aspect('equal', 'box')

    ax1.scatter(centx,centy, s=20, c = 'k', marker='x',  alpha = 1)
    ax2.scatter(centy,centz, s=20, c = 'k', marker='x',  alpha = 1)
    ax3.scatter(centz,centx, s=20, c = 'k', marker='x',  alpha = 1)

    fig.canvas.draw()

def update(frame):
    getNewInput()
    redrawGraphs()


def getNumSamples():
    global numSamples
    validInput = False
    while not validInput:
        numSamples = input("Number of samples: ")
        try:
            numSamples = int(numSamples)
            if numSamples < 1 or 30 < numSamples:
                raise TypeError("Value must be between 1 and 30")
            validInput = True
        except:
            print("Invalid input. Provide a number between 1 and 30\n")
            validInput = False

def getOffsets(dataA, dataB):
    centA = np.zeros(numSamples)
    centB = np.zeros(numSamples)
    for i in range(0, numSamples):
        angle = 180 * i / numSamples
        angle_radians = np.deg2rad(angle)
        alt_dataA = np.multiply(dataA, np.cos(angle_radians)) + np.multiply(dataB, np.sin( angle_radians))
        alt_dataB = np.multiply(dataB, np.cos(angle_radians)) + np.multiply(dataA, np.sin(-angle_radians))
        localOffA = (min(alt_dataA) + max(alt_dataA)) / 2
        localOffB = (min(alt_dataB) + max(alt_dataB)) / 2
        centA[i] = np.multiply(localOffA, np.cos(-angle_radians)) + np.multiply(localOffB, np.sin(-angle_radians))
        centB[i] = np.multiply(localOffB, np.cos(-angle_radians)) - np.multiply(localOffA, np.sin(-angle_radians))
    return centA, centB

        

def findOffsets():
    getNumSamples()
    centx_y, centy_x = getOffsets(x_data, y_data)
    centy_z, centz_y = getOffsets(y_data, z_data)
    centz_x, centx_z = getOffsets(z_data, x_data)
    redrawGraphs()
    ax1.scatter(centx_y,centy_x, s=30, c = 'y', marker='x',  alpha = 1)
    ax2.scatter(centy_z,centz_y, s=30, c = 'c', marker='x',  alpha = 1)
    ax3.scatter(centz_x,centx_z, s=30, c = 'm', marker='x',  alpha = 1)
    totalOffsetx = (centx_y.mean() + centx_z.mean()) / 2
    totalOffsety = (centy_x.mean() + centy_z.mean()) / 2
    totalOffsetz = (centz_x.mean() + centz_y.mean()) / 2
    ax1.scatter([totalOffsetx],[totalOffsety], s=30, c = 'k', marker='.',  alpha = 1)
    ax2.scatter([totalOffsety],[totalOffsetz], s=30, c = 'k', marker='.',  alpha = 1)
    ax3.scatter([totalOffsetz],[totalOffsetx], s=30, c = 'k', marker='.',  alpha = 1)
    fig.canvas.draw()
    print("x offset: ", totalOffsetx)
    print("y offset: ", totalOffsety)
    print("z offset: ", totalOffsetz)
    print()



try:
    # use interval of 12 to match IMU update of ~90 hz
    ani = FuncAnimation(fig, update, interval=12, cache_frame_data=False)
    plt.show()
except KeyboardInterrupt:
    print("")
    ani.event_source.stop()
    pass
finally:
    findOffsets()

try:
    plt.show()
finally:
    ser.close()

