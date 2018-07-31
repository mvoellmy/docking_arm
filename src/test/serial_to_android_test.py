import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from drawnow import *
import numpy as np
import time

# Serial
params = {
    "baudrate": 9600,
    "board": "micro",
    "port": '/dev/cu.usbmodem1421',
    "data_buffer": 200
}

pressure = np.array([0, 0, 0, 0])
pressures = []

# Plotting
style.use('fivethirtyeight')
plt.ion()
fig = plt.figure()

# Saving
path_data = '/Users/miro/Documents/Repositories/docking_arm/data/pressure/'

print("Welcome to the pressure readout.\n What do you want to do?")
print("1. Show live pressure values")
print("2. Save live pressure values to file")
# action = input()


def make_fig():
    hist_plt = fig.add_subplot(1, 2, 1)
    cups_plt = fig.add_subplot(1, 2, 2)
    hist_plt.plot(pressures)

    square_width = 1

    cups_plt.axis('off')
    cups_plt.set_aspect('equal')
    cups_plt.set_xlim([-square_width, square_width])
    cups_plt.set_ylim([-square_width, square_width])

    cups_x = [-square_width/2, square_width/2, -square_width/2, square_width/2]
    cups_y = [square_width/2, square_width/2, -square_width/2, -square_width/2]

    cups_plt.plot(cups_x, cups_y, marker='o', markersize='80', linestyle='None', rasterized='True')

    for cup_pressure, x, y in zip(pressure, cups_x, cups_y):
        cups_plt.annotate(cup_pressure, xy=(x, y), horizontalalignment='center', verticalalignment='center')


with serial.Serial(params['port'], params['baudrate'], timeout=1) as ser:
    try:
        while True:
            # Read Serial
            line = str(ser.readline())
            line = line.replace("b'", "")
            line = line.replace("\\r\\n'", "")

            output = line.split(":", 1)
            if int(output[0]) < 4:
                pressure[int(output[0])] = float(output[1])

                pressures.append(np.copy(pressure))

                # Plot Data
                drawnow(make_fig)  # Call drawnow to update our live graph
                plt.pause(.000001)

            if len(pressures) > params['data_buffer']:
                pressures.pop(0)


    except KeyboardInterrupt:
        print("\n##################")
        print("Monitoring exited!")

if input("Save Pressure Data? [y/n]").lower() == 'y':
    time_name = time.strftime("%Y-%m-%d-%H_%M_%S")
    pressure_name = path_data + time_name + '.csv'

    with open(pressure_name, 'w') as file:
        file.write(repr(pressures))