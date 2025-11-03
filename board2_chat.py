# HW5 For ETH Mobile Computing and Wireless Networking
# board2_chat.py

from board_basic_functions import setup, listen, transmit

def __main__():
    target_address, serial_connection = setup("COM6")
    
    while(True):
        listen(serial_connection)
        transmit(target_address, serial_connection)