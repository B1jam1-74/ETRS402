import serial
import time

PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

billy = []
fini = True
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Attendre que la connexion soit stable
while fini:
    if ser.in_waiting > 0:
        if ser.readline().decode('utf-8').strip() == '9999':
            billy = []
            for i in range(270):
                billy.append( ser.readline().decode('utf-8').strip() )
            print(billy)
            fini = False