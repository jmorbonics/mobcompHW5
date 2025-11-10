# HW5 For ETH Mobile Computing and Wireless Networking
# board1_chat.py

from board_basic_functions import setup, listen, transmit
import time

def main():
    print("Booting up board 1")
    target_address, serial_connection = setup("COM5")

    while(True):
        received_message = transmit(target_address, serial_connection)
        time.sleep(0.5)
        listen(serial_connection)
        time.sleep(0.5)

if __name__ == "__main__":
    main()

