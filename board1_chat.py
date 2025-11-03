# HW5 For ETH Mobile Computing and Wireless Networking
# Contributors
    # Jack Morby (25-941-373)
    # Rashi Ojha (25-910-506)

import serial
import time
import sys

def setup():
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
    
    return target_address, s

# Read from the device’s serial port
def listen(s):
    print("Listening for incoming messages...")
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

def transmit(target, s):
    print("You can now start sending messages. Type your message and press Enter to send.")
    try:
        while True:
            message = input("Enter message: ")
            full_message = "m[" + message + "\0," + target + "]\n"
            s.write(str.encode(full_message))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()


def __main__():
    target_address, serial_connection = setup()
    while(True):
        transmit(target_address, serial_connection)
        listen(serial_connection)
        
