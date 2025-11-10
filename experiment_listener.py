# HW5 For ETH Mobile Computing and Wireless Networking
# board1_chat.py

from board_basic_functions import setup, listen, transmit
import time
import matplotlib.pyplot as plt

def main():
    print("Booting up board 1")
    target_address, serial_connection = setup("COM5")
    time_threshold = 20  # seconds
    start_time = time.time()
    elapsed_time = 0
    counter = 0
    rates = []
    while(True):
        counter += 1
        listen(serial_connection)
        if counter == 0:
            start_time = time.time()
        elapsed_time = time.time() - start_time
        rates.append(elapsed_time / counter)
        print("Elapsed Time: ", elapsed_time)
        if elapsed_time >= time_threshold:  # Stop after 10 seconds
            print("Time threshold reached. Exiting...")
            break
    # transmission_rate = time_threshold / counter
    print("Transmission time / transmisssion: ", rates)

    # Generate graph
    plt.plot(rates, marker='o')
    plt.title("Transmission Time per Transmission")
    plt.xlabel("Transmission Count")
    plt.ylabel("Time per Transmission (s)")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()

