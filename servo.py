import serial
import time

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
	port="COM2",
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

ser.close()
ser.open()
start = chr(255) #starting character at the beginning of each packet

#servo 0 
    #20 to 68 for up and down servo (20 is 90 degrees up, 68 is about 45 degrees down)

for i in range(1,10):
    #move to position 1
    #servo 1 command
    packet = ''.join([start, chr(1), chr(0)])
    ser.write(packet)
    #wait some time between commands
    time.sleep(.02)
    #servo 0 command
    packet = ''.join([start, chr(0), chr(50)])
    ser.write(packet)
    #wait some time to let servos get into position
    time.sleep(2)

    #move to position 2
    #servo 1 command
    packet = ''.join([start, chr(1), chr(30)])
    ser.write(packet)
    #wait some time between commands
    time.sleep(.02)
    #servo 0 command
    packet = ''.join([start, chr(0), chr(20)])
    ser.write(packet)
    #wait some time to let servos get into position
    time.sleep(2)    

    #move to position 3
    #servo 1 command
    packet = ''.join([start, chr(1), chr(80)])
    ser.write(packet)
    #wait some time between commands
    time.sleep(.02)
    #servo 0 command
    packet = ''.join([start, chr(0), chr(70)])
    ser.write(packet)
    #wait some time to let servos get into position
    time.sleep(2) 
        
ser.close()
		
