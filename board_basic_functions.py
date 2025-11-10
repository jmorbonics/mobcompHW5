# HW5 For ETH Mobile Computing and Wireless Networking
# board_basic_functions.py

import serial
import sys
import time
import re

# Setup the arudino board configs
def setup(COM):
    # Connect to board
    print("Starting Board Chat Program...")
    s = serial.Serial(COM, 115200, timeout=1)
    time.sleep(2)  # Give device time to start up

    # Set device address
    device_address = input("Enter desired personal device address (e.g., AB, CD): ").strip().upper()
    print("Setting address to \"" + device_address + "\" ...")
    s.write(str.encode("a[" + device_address + "]\n"))
    time.sleep(0.1)
    s.write(str.encode("a\n"))  # Print device address to verify
    time.sleep(0.1)

    # Configure board
    s.write(str.encode("c[1,0,5]\n"))  # Set number of retransmissions to 5
    time.sleep(0.1)
    s.write(str.encode("c[0,1,30]\n"))  # Set FEC threshold to 30
    time.sleep(0.1)

    listen_for(s, "c[0,1,30]") # wait for confirmation of configurations

    # Set target device address
    target_address = input("Enter target device address to send messages to (e.g., AB, CD): ").strip().upper()
    
    return target_address, s


# Receive message
def listen(s):
    print("Listening for incoming messages...")
    try:
        message = ""
        # Regular expression to capture the content inside m[R,D,<content>]
        pattern = r"m\[R,D,(.*)\]"  
        while True:  # Continuously read data
            byte = s.read(1)  # Read one byte (blocks until data is available or timeout occurs)
            if byte:
                val = chr(byte[0])  # Convert the byte to a character
                if val == '\n':  # If the termination character is received
                    # print(message)  # Print the complete message (for debugging)
                    if message == "m[D]":
                        print("Transmission done")
                        message = ""
                        return "NA"
                    match = re.match(pattern, message)
                    if match:
                        content = match.group(1)
                        print("Received message content: " + content)
                        return content
                    message = ""
                else:
                    message += val  # Append the character to the message buffer
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

def listen_for(s, key):
    try:
        message = ""
        while True:  # Continuously read data
            byte = s.read(1)  # Read one byte (blocks until data is available or timeout occurs)
            if byte:
                val = chr(byte[0])  # Convert the byte to a character
                if val == '\n':  # If the termination character is received
                    # print(message)  # Print the complete message (for debugging)
                    if message == "m[D]":
                        print("Transmission done")
                        message = ""
                        break
                    if message == key:
                        message = ""
                        break
                    message = ""
                else:
                    message += val  # Append the character to the message buffer
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

# Send message
def transmit(target, s):
    print("Beginning message transmission process...")
    try:
        message = input("Type your message and press Enter to send: ")
        full_message = "m[" + message + "\0," + target + "]\n"
        s.write(str.encode(full_message))
        listen_for(s, "m[D]")  # Listen to arduino for transmission termination 
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

# Send message
def transmit_message(target, s, message):
    print("Beginning message transmission process...")
    try:
        full_message = "m[" + message.hex() + "\0," + target + "]\n"
        s.write(str.encode(full_message))
        listen_for(s, "m[D]")  # Listen to arduino for transmission termination 
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

if __name__ == "__main__":
    print("This is a module for listening to serial ports.")