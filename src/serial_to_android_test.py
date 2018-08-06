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
    "send_rate": 40                 # [Hz] The arduino script sends information about one suction cup every 25 ms
}

pressure = np.array([0, 0, 0, 0])
pressures = []

# Plotting
style.use('fivethirtyeight')
plt.ion()
fig = plt.figure()
counts_since_draw = 0
plot_time = 10
update_rate = 4                   # [Hz] The update rate of the plot
history_duration = 30             # [s] how long will the plot display the pressure history
history_frames = int(history_duration*params["send_rate"]/4)


# Saving
path_data = '/Users/miro/Documents/Repositories/docking_arm/data/pressure/'

print("Welcome to the pressure readout.\n What do you want to do?")
print("1. Show live pressure values")
print("2. Save live pressure values to file")
# action = input()


def make_fig():
    fig.suptitle("Vacuum Status")
    hist_plt = fig.add_subplot(1, 2, 1)
    cups_plt = fig.add_subplot(1, 2, 2)
    hist_plt.plot(pressures[-history_frames:])

    hist_plt.legend("1234", loc="lower right")

    hist_plt.set_xlabel("s/10")
    hist_plt.set_ylabel("mbar")


    # Plotting parameters
    square_width = 1
    pressure_saturation = 800
    name_offset = 0.4

    cups_plt.axis('off')
    cups_plt.set_aspect('equal')
    cups_plt.set_xlim([-square_width, square_width])
    cups_plt.set_ylim([-square_width, square_width])

    cups_x = [-square_width/2, square_width/2, -square_width/2, square_width/2]
    cups_y = [square_width/2, square_width/2, -square_width/2, -square_width/2]

    cup_names = [1, 2, 3, 4]

    for cup_pressure, cup_name, x, y in zip(pressure, cup_names, cups_x, cups_y):
        cup_color = (max(0, (pressure_saturation+cup_pressure)/pressure_saturation), min(1, cup_pressure/-pressure_saturation), 0)
        cups_plt.plot(x, y, marker='o', markersize='80', linestyle='None', rasterized='True', color=cup_color)
        cups_plt.annotate(cup_pressure, xy=(x, y), horizontalalignment='center', verticalalignment='center', fontsize=12)
        cups_plt.annotate(cup_name, xy=(x-name_offset, y+name_offset), horizontalalignment='center', verticalalignment='center', fontsize=8)


with serial.Serial(params['port'], params['baudrate'], timeout=1) as ser:
    try:
        while True:
            # start_time = time.time()

            # Read Serial
            line = ser.readline()
            line = line.decode("utf-8")

            output = line.split(":", 1)
            if int(output[0]) < 5:
                pressure[int(output[0])-1] = float(output[1])

                if int(output[0]) == 4:
                    pressures.append(np.copy(pressure).tolist())

                if counts_since_draw > params['send_rate']/update_rate:
                    # Plot Data
                    drawnow(make_fig)  # Call drawnow to update our live graph
                    plt.pause(.00000001)

                    counts_since_draw = 0

            counts_since_draw += 1

            # print(time.time() - start_time)

    except KeyboardInterrupt:
        print("\n##################")
        print("Monitoring exited!")

if input("Save Pressure Data? [y/n]\n").lower() == 'y':
    time_name = time.strftime("%Y-%m-%d-%H_%M_%S")
    pressure_name = path_data + time_name + '.csv'

    with open(pressure_name, 'w') as file:
        file.write(repr(pressures))