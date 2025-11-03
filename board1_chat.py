# HW5 For ETH Mobile Computing and Wireless Networking
# board1_chat.py

from board_basic_functions import setup, listen, transmit

def __main__():
    target_address, serial_connection = setup("COM5")

    while(True):
        transmit(target_address, serial_connection)
        listen(serial_connection)
    

        
