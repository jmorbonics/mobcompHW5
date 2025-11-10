# HW5 For ETH Mobile Computing and Wireless Networking
# experiment_transmitter.py

from board_basic_functions import setup, listen_for_line, transmit_message, setup_logging
import time
import os
import logging

# Set up dedicated experiment log
logger = setup_logging("transmitter_log.log")
# Log header: Timestamp of event, Event Type, Sequence Number, Transmission Start Time (local float), Packet Send Time (embedded ms)
logger.info("Local_Timestamp,Event_Type,Sequence_Number,Local_Tx_Start_Time_s,Packet_Send_Time_ms")

def main():
    print("Booting up transmitter (Board 2)")
    # Setup returns target_address, serial_connection, setup_logger (unused here, as we use 'logger')
    target_address, serial_connection, _ = setup("COM6") 
    
    payload_size = 100  # bytes
    sequence_number = 0
    
    print("Starting experiment: Sending saturation traffic for 5 seconds.")
    # Use a longer duration for better results
    time_threshold = 5 # seconds
    start_experiment_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_experiment_time
        if elapsed_time >= time_threshold:
            print("Time threshold reached. Exiting...")
            break

        # 1. Generate unique message (random bytes)
        # Using a sequence number as part of the data helps verify packet order/loss
        payload = os.urandom(payload_size)
        
        # 2. Transmit the message and get the exact local start time and embedded timestamp
        # transmit_message handles the m[D] wait (ACK/retransmissions handled by board firmware)
        local_tx_start_time, packet_send_time_ms = transmit_message(
            target_address, 
            serial_connection, 
            payload
        )
        
        # 3. Log the successful transmission attempt
        logger.info(
            f"TX_ATTEMPT,{sequence_number},{local_tx_start_time},{packet_send_time_ms}"
        )
        
        # 4. Implement saturation traffic: send a new message immediately
        # The 'transmit_message' function waits for the m[D] command from the board,
        # which means the next message is sent immediately after the previous one is *done*.
        # The required 10ms pause between commands is handled by the initial 
        # 'transmit_message' implementation (waiting for m[D] includes micro-controller processing).
        
        sequence_number += 1
        
    print(f"Total packets attempted: {sequence_number}")


if __name__ == "__main__":
    main()