import serial

ser = serial.Serial(
    port = "COM3",
    baudrate=9600,
    timeout=1
)

while True:
    line = ser.readline()
    if line:
        print(line.decode('utf-8').strip())
    else:
        print("Nothing detected")