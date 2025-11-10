# HW5 For ETH Mobile Computing and Wireless Networking
# experiment_receiver.py

from board_basic_functions import setup, listen_for_line, setup_logging
import time
import re
import csv
import logging

# Set up dedicated experiment log
logger = setup_logging("receiver_log.log")
# Log header: Timestamp of event, Event Type, Serial Line Content
logger.info("Local_Timestamp,Event_Type,Serial_Line_Content")

def parse_received_message(line):
    """
    Parses a serial line to extract the embedded timestamp and payload.
    Expected message format from board: m[R,D,<hex_timestamp>|<hex_payload>]
    """
    # Regex to capture the content inside m[R,D,<content>]
    pattern = r"m\[R,D,(.*)\]"
    match = re.match(pattern, line)

    if match:
        full_hex_data = match.group(1)
        
        # The data is in hex, need to decode
        try:
            # The data format is <hex_timestamp>|<hex_payload>
            if "|" in full_hex_data:
                parts = full_hex_data.split('|')
                if len(parts) >= 2:
                    # The first part is hex-encoded timestamp string
                    hex_timestamp = parts[0]
                    
                    # The rest is the payload (can be multiple parts if payload contained '|')
                    # Recombine the rest of the parts for payload content
                    hex_payload = '|'.join(parts[1:]) 
                    
                    # Decode timestamp hex to string, then to int (ms)
                    timestamp_str = bytes.fromhex(hex_timestamp).decode('utf-8')
                    send_time_ms = int(timestamp_str)
                    
                    # Log raw hex payload for verification (optional)
                    # payload_bytes = bytes.fromhex(hex_payload)
                    
                    return send_time_ms
        except Exception as e:
            logger.error(f"Error parsing hex data: {e} from line: {line}")
            return None
    return None

def main():
    print("Booting up receiver (Board 1)")
    # Setup returns target_address, serial_connection, setup_logger
    _, serial_connection, _ = setup("COM5")
    
    # --- CSV Setup ---
    csv_filename = "experiment_results.csv"
    csv_file = open(csv_filename, 'w', newline='')
    csv_writer = csv.writer(csv_file)
    # CSV Header: Sequence Number, Send Time (ms), Receive Time (ms), End-to-End Delay (ms)
    csv_writer.writerow(['Sequence_Number', 'Send_Time_ms', 'Receive_Time_ms', 'End_to_End_Delay_ms'])
    print(f"Results will be saved to {csv_filename}")
    
    sequence_number = 0
    print("Starting experiment: Listening for messages.")
    
    try:
        while True:
            # Read a full line from the serial port
            line = listen_for_line(serial_connection)
            
            # Record the exact time the message (or command) was fully received
            receive_time_ms = int(time.time() * 1000)
            
            # Log the raw line for debugging/verification
            logger.info(f"SERIAL_LINE_IN,{line}")

            if line.startswith("m[R,D,"):
                # This is a received data packet
                send_time_ms = parse_received_message(line)
                
                if send_time_ms is not None:
                    # Calculate End-to-End Delay
                    delay_ms = receive_time_ms - send_time_ms
                    
                    # Log to CSV
                    csv_writer.writerow([sequence_number, send_time_ms, receive_time_ms, delay_ms])
                    
                    # Log to file
                    logger.info(
                        f"PACKET_RECEIVED,{sequence_number},{send_time_ms},{receive_time_ms},{delay_ms}"
                    )
                    
                    sequence_number += 1
                    
            elif line == "m[D]":
                # This is a transmission done notification (shouldn't happen on receiver unless it's an ACK)
                pass # Ignore 'transmission done' on receiver for data collection
                
            elif line:
                # Other messages (e.g., config, address)
                print(f"Board Info: {line}")
                
    except KeyboardInterrupt:
        print("\nStopping listener...")
    finally:
        csv_file.close()
        print(f"Total received packets: {sequence_number}")
        print(f"Data saved to {csv_filename}")


if __name__ == "__main__":
    main()