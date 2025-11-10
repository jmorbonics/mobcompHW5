# HW5 For ETH Mobile Computing and Wireless Networking
# board2_chat.py

from board_basic_functions import setup, listen, transmit
import time

def main():
    print("Booting up board 2")
    target_address, serial_connection = setup("COM5")
    
    while(True):
        print("Starting listening")
        received_message = listen(serial_connection)  # Use received message for GUI
        time.sleep(0.5)
        transmit(target_address, serial_connection)
        time.sleep(0.5)

if __name__ == "__main__":
    main()