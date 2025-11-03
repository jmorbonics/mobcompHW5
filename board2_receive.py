# HW5 For ETH Mobile Computing and Wireless Networking
# Contributors
    # Jack Morby (25-941-373)
    # Rashi Ojha (25-...)

import serial
import sys
import time



# Open the serial port (ensure the same port and baud rate as the writing program)
s = serial.Serial('COM6', 115200, timeout=1)

time.sleep(2)  # Give the device some time to start up
s.write(str.encode("a[CD]\n"))  # Set the device address to AB
time.sleep(0.1)

s.write(str.encode("a\n"))  # Print the device address to verify it was set correctly
time.sleep(0.1)

s.write(str.encode("c[1,0,5]\n"))  # Set number of retransmissions to 5
time.sleep(0.1)

s.write(str.encode("c[0,1,30]\n"))  # Set FEC threshold to 30
time.sleep(0.1)

# Read from the device’s serial port
try:
    message = ""
    while True:  # Continuously read data
        byte = s.read(1)  # Read one byte (blocks until data is available or timeout occurs)
        if byte:  # If data is received
            val = chr(byte[0])  # Convert the byte to a character
            if val == '\n':  # If the termination character is received
                print(message)  # Print the complete message
                message = ""  # Reset the message buffer
            else:
                message += val  # Append the character to the message buffer
except KeyboardInterrupt:
    print("\nExiting...")
    s.close()  # Close the serial port on exit
    sys.exit()