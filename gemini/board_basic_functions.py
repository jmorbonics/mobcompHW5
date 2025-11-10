# HW5 For ETH Mobile Computing and Wireless Networking
# board_basic_functions.py

import serial
import sys
import time
import re
import logging

# --- Logging Setup ---
def setup_logging(filename):
    """Sets up a file logger for the script."""
    # Create logger
    logger = logging.getLogger('ExperimentLogger')
    logger.setLevel(logging.INFO)

    # Create file handler which logs even debug messages
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s,%(message)s')
    fh.setFormatter(formatter)

    # Add the handlers to the logger
    if not logger.handlers: # Avoid adding handlers multiple times
        logger.addHandler(fh)
        
    return logger

# --- Core Board Functions ---
def setup(COM):
    # Connect to board
    print("Starting Board Chat Program...")
    # Using 'setup_logging' for general board operations log
    logger = setup_logging(f"board_setup_log_{COM}.log")
    logger.info(f"Connecting to {COM}")
    
    s = serial.Serial(COM, 115200, timeout=1)
    time.sleep(2)  # Give device time to start up
    logger.info("Serial connection established.")

    # Set device address
    device_address = input("Enter desired personal device address (e.g., AB, CD): ").strip().upper()
    print("Setting address to \"" + device_address + "\" ...")
    s.write(str.encode("a[" + device_address + "]\n"))
    time.sleep(0.1)
    s.write(str.encode("a\n"))  # Print device address to verify
    time.sleep(0.1)
    logger.info(f"Set own address to {device_address}")

    # Configure board (Retries: 5, FEC: 30)
    s.write(str.encode("c[1,0,5]\n"))
    time.sleep(0.1)
    s.write(str.encode("c[0,1,30]\n"))
    time.sleep(0.1)
    logger.info("Set configurations c[1,0,5] and c[0,1,30]")

    listen_for(s, "c[0,1,30]") # wait for confirmation of configurations

    # Set target device address
    target_address = input("Enter target device address to send messages to (e.g., AB, CD): ").strip().upper()
    logger.info(f"Target address set to {target_address}")
    
    return target_address, s, logger


# Receive message - MODIFIED to return the raw serial line for further processing
def listen_for_line(s):
    """Continuously reads from serial until a full line ('\n') is received."""
    message = ""
    try:
        while True:
            byte = s.read(1)
            if byte:
                val = chr(byte[0])
                if val == '\n':
                    return message
                else:
                    message += val
    except KeyboardInterrupt:
        print("\nExiting...")
        s.close()
        sys.exit()

def listen_for(s, key):
    """Listens for a specific key/command confirmation from the board."""
    while True:
        message = listen_for_line(s)
        if message == key:
            break

# Send message with current timestamp
def transmit_message(target, s, payload_bytes):
    """
    Sends a message containing a current Unix timestamp prepended to the payload.
    Returns the exact transmission start time (float) for delay calculation.
    """
    # Get current time as Unix timestamp (milliseconds)
    send_time_ms = int(time.time() * 1000)
    
    # Prepend timestamp to payload, separated by a unique delimiter (e.g., '|')
    # The message format will be: <timestamp_ms>|<payload_hex>
    timestamp_str = str(send_time_ms)
    
    # Encode timestamp as hex and combine with payload hex
    timestamp_hex = timestamp_str.encode('utf-8').hex()
    full_hex_payload = timestamp_hex + "|" + payload_bytes.hex()
    
    # Construct the full command: m[<hex_payload>\0,<target>]\n
    # Note: The board may interpret '|' as part of the data, which is fine
    # as long as the receiver knows how to parse it.
    full_message_command = "m[" + full_hex_payload + "\0," + target + "]\n"
    
    # Log transmission attempt time
    tx_start_time = time.time()
    s.write(str.encode(full_message_command))
    
    # Wait for the "transmission done" command m[D] from the board
    listen_for(s, "m[D]")
    
    return tx_start_time, send_time_ms

if __name__ == "__main__":
    print("This is a module for listening to serial ports.")