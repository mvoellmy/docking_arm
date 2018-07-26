import serial

params = {
    "baudrate": 9600,
    "board": "micro",
    "port": '/dev/cu.usbmodem1421'
}

pressure = [0, 0, 0, 0]

with serial.Serial(params['port'], params['baudrate'], timeout=1) as ser:
    while True:
        line = str(ser.readline())
        line = line.replace("b'", "")
        line = line.replace("\\r\\n'", "")

        output = line.split(":", 1)
        pressure[int(output[0])] = output[1]

        if int(output[0]) == 3:
            print("Pressure in Cups [mbar]: " + str(pressure))

        # print(line)
