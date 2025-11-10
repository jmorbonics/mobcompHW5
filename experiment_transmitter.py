# HW5 For ETH Mobile Computing and Wireless Networking
# experiment_transmitter.py

from board_basic_functions import setup, listen, transmit, transmit_message
import time
import os

def main():
    print("Booting up board 2")
    target_address, serial_connection = setup("COM6")
    
    payload_size = 50  # bytes
    message = os.urandom(payload_size)  # Generate 100 random bytes

    
    print("Starting experiment")
    time.sleep(0.1)
    while True:
        transmit_message(target_address, serial_connection, message)
        time.sleep(0.01)
        


if __name__ == "__main__":
    main()