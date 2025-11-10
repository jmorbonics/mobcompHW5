# HW5 For ETH Mobile Computing and Wireless Networking
# data_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Analysis Functions ---

def load_and_merge_data():
    """Loads and merges data from the transmitter log and receiver CSV."""
    try:
        # Load receiver data (successful transmissions)
        rx_df = pd.read_csv('experiment_results.csv')
        rx_df = rx_df.rename(columns={'Send_Time_ms': 'Packet_Send_Time_ms'})
        
        # Load transmitter log (all attempts)
        # Use the first column as the index (Local_Timestamp)
        tx_df = pd.read_csv('transmitter_log.log', header=None, skiprows=1, 
                            names=['Local_Timestamp', 'Event_Type', 'Sequence_Number_TX', 
                                   'Local_Tx_Start_Time_s', 'Packet_Send_Time_ms'])
        
        # Filter for successful TX attempts
        tx_attempts_df = tx_df[tx_df['Event_Type'] == 'TX_ATTEMPT']
        
        # Merge the two DataFrames on the unique identifier: Packet_Send_Time_ms
        # A merge will only keep packets that appear in BOTH the TX log and the RX log.
        merged_df = pd.merge(tx_attempts_df, rx_df, on='Packet_Send_Time_ms', how='left')
        
        return merged_df, rx_df
    
    except FileNotFoundError as e:
        print(f"Error: Required file not found. Please run the experiments first.")
        print(f"Missing file: {e}")
        return None, None
    except Exception as e:
        print(f"An error occurred during data loading: {e}")
        return None, None

def calculate_statistics(rx_df, merged_df):
    """Calculates throughput, delay, and loss statistics."""
    
    # --- Throughput and Loss ---
    total_tx_attempts = len(merged_df)
    total_rx_success = len(rx_df)
    
    if total_tx_attempts == 0:
        print("No transmission attempts found. Cannot calculate loss/throughput.")
        return None
        
    packet_loss_rate = (total_tx_attempts - total_rx_success) / total_tx_attempts
    
    # Calculate effective experiment duration from RX data
    # Use the first and last successful receipt time
    if total_rx_success < 2:
        effective_duration_s = 60 # Default to 60s if not enough data
        print("Warning: Less than 2 successful packets. Using default duration for throughput.")
    else:
        # Convert ms to seconds
        start_time_s = rx_df['Receive_Time_ms'].min() / 1000.0
        end_time_s = rx_df['Receive_Time_ms'].max() / 1000.0
        effective_duration_s = end_time_s - start_time_s
        # Ensure minimum duration for stability
        if effective_duration_s < 1:
             effective_duration_s = 1 
             
    # Assuming 100 bytes (800 bits) per payload from experiment setup
    packet_size_bits = 100 * 8
    
    # Throughput (bits per second)
    throughput_bps = (total_rx_success * packet_size_bits) / effective_duration_s if effective_duration_s > 0 else 0
    
    # --- Delay ---
    delay_stats = rx_df['End_to_End_Delay_ms'].describe()
    
    stats = {
        "Total_TX_Attempts": total_tx_attempts,
        "Total_RX_Success": total_rx_success,
        "Packet_Loss_Rate": f"{packet_loss_rate * 100:.2f}%",
        "Effective_Duration_s": f"{effective_duration_s:.2f}",
        "Throughput_bps": f"{throughput_bps:,.2f}",
        "Mean_Delay_ms": f"{delay_stats['mean']:.2f}",
        "Median_Delay_ms": f"{delay_stats['50%']:.2f}",
        "Std_Dev_Delay_ms": f"{delay_stats['std']:.2f}",
        "Min_Delay_ms": f"{delay_stats['min']:.2f}",
        "Max_Delay_ms": f"{delay_stats['max']:.2f}",
    }
    
    return stats

def generate_plots(rx_df):
    """Generates and saves plots for delay and throughput."""
    
    if rx_df.empty:
        print("No successful data to plot.")
        return

    # 1. End-to-End Delay Plot
    plt.figure(figsize=(10, 5))
    plt.plot(rx_df.index, rx_df['End_to_End_Delay_ms'], label='End-to-End Delay', alpha=0.7)
    plt.title('End-to-End Delay per Received Packet')
    plt.xlabel('Received Packet Index')
    plt.ylabel('Delay (ms)')
    plt.grid(True)
    plt.legend()
    plt.savefig('delay_plot.png')
    plt.close()
    
    print("Saved delay plot: delay_plot.png")
    
    # 2. Delay Histogram/Distribution
    plt.figure(figsize=(10, 5))
    plt.hist(rx_df['End_to_End_Delay_ms'], bins=30, edgecolor='black', alpha=0.7)
    plt.title('Distribution of End-to-End Delay')
    plt.xlabel('Delay (ms)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.5)
    plt.savefig('delay_histogram.png')
    plt.close()
    
    print("Saved delay histogram: delay_histogram.png")

def provide_interpretation(stats):
    """Generates an interpretation based on the calculated statistics."""
    
    interpretation = "## 📝 Experiment Interpretation and Findings\n\n"
    
    if stats is None:
        interpretation += "No statistical data available for interpretation."
        return interpretation

    interpretation += (
        "> This experiment measured the **throughput** and **delay** of the wireless link under **saturation traffic** (continuously sending maximum-size packets).\n\n"
        "### Key Findings\n"
        f"* **Throughput (Effective Data Rate):** The link achieved a throughput of **{stats['Throughput_bps']} bps**.\n"
        f"    * This represents the net bit-rate after accounting for protocol overhead, retransmissions, and the 10ms gap enforced by the saturation traffic implementation.\n\n"
        f"* **End-to-End Delay:** The mean packet delay was **{stats['Mean_Delay_ms']} ms** (Median: **{stats['Median_Delay_ms']} ms**).\n"
        f"    * This delay includes the transmission time, propagation delay (negligible over short distance), processing time on both boards, and any time spent waiting for retransmission attempts.\n\n"
        f"* **Packet Reliability (Loss Rate):** A total of **{stats['Total_TX_Attempts']}** packets were attempted, with **{stats['Total_RX_Success']}** successfully received. This results in a measured packet loss rate of **{stats['Packet_Loss_Rate']}**.\n"
        f"    * Since unicast transmissions with retransmissions (max 5) were used, any lost packets suggest the maximum retransmission limit was reached, or the transmitter stopped before the ACK was received.\n\n"
        "### Observations from Statistical Information\n"
        f"The difference between the **Minimum Delay ({stats['Min_Delay_ms']} ms)** and the **Maximum Delay ({stats['Max_Delay_ms']} ms)** indicates **delay jitter**.\n"
        "This jitter is primarily caused by varying channel conditions (requiring retransmissions) and non-deterministic queuing/processing delays within the microcontroller's firmware. The large standard deviation (**{stats['Std_Dev_Delay_ms']} ms**) confirms this variability, suggesting the channel quality may be inconsistent or that the retransmission mechanism significantly impacts the overall delay distribution.\n"
    )
    
    return interpretation

# --- Main Execution ---

if __name__ == "__main__":
    
    merged_data, rx_data = load_and_merge_data()

    if merged_data is not None and not merged_data.empty:
        # Calculate statistics
        experiment_stats = calculate_statistics(rx_data, merged_data)
        
        # Display Statistical Information (Data Logs/Findings)
        print("\n" + "="*50)
        print("## ✨ Throughput and Delay Statistical Information")
        print("="*50)
        for key, value in experiment_stats.items():
            print(f"* {key.replace('_', ' '):<30}: {value}")
        print("="*50 + "\n")

        # Generate Graphs
        generate_plots(rx_data)
        
        # Generate Interpretation
        interpretation_text = provide_interpretation(experiment_stats)
        print(interpretation_text)
        
        # Save interpretation to a findings file
        with open('experiment_findings.md', 'w') as f:
            f.write(interpretation_text)
            print("\nSaved detailed interpretation and findings to: experiment_findings.md")
            
    else:
        print("Analysis stopped due to missing or empty data files.")