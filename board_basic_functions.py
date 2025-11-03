# HW5 For ETH Mobile Computing and Wireless Networking
# board_basic_functions.py


import serial
import sys
import time

def setup(COM):
    # Connect to board
    print("Starting Board Chat Program...")
    # Open the serial port (ensure the same port and baud rate as the writing program)
    s = serial.Serial(COM, 115200, timeout=1)
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
                    # Quit
                    break
                else:
                    message += val  # Append the character to the message buffer
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

def transmit(target, s):
    try:
        while True:
            message = input("You can now start sending a message. Type your message and press Enter to send: ")
            full_message = "m[" + message + "\0," + target + "]\n"
            s.write(str.encode(full_message))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()  # Close the serial port on exit
        sys.exit()

if __name__ == "__main__":
    print("This is a module for listening to serial ports.")