# HW5 For ETH Mobile Computing and Wireless Networking
# Contributors
    # Jack Morby (25-941-373)
    # Rashi Ojha (25-910-506)

import serial
import time
import sys
import serial

# Connect to board
print("Starting Board 1 Chat Program...")
# Open the serial port (ensure the same port and baud rate as the writing program)
s = serial.Serial('COM5', 115200, timeout=1)
time.sleep(2)  # Give the device some time to start up

# Set device address
device_address = input("Enter desired personal device address (e.g., AB, CD): ").strip().upper()
s.write(str.encode("a[" + device_address + "]\n"))
time.sleep(0.1)
print("Address set:")
s.write(str.encode("a\n"))  # Print the device address to verify it was set correctly
time.sleep(0.1)

# Configure board
s.write(str.encode("c[1,0,5]\n"))  # Set number of retransmissions to 5
time.sleep(0.1)
s.write(str.encode("c[0,1,30]\n"))  # Set FEC threshold to 30
time.sleep(0.1)

# Set target device address
target_address = input("Enter target device address to send messages to (e.g., AB, CD): ").strip().upper()
# Send a test message to the target device
s.write(str.encode("m[hello world!\0," + target_address + "]\n")) #send message to device with address CD  


print("\nExiting...")
s.close()  # Close the serial port on exit
sys.exit()
