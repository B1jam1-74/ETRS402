import serial
import time
import os
import numpy as np

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
TOTAL_SCANS = 50

# Initialize data structure
data = []
for i in range(90):
    data.append([])

# Function to collect the data
def collect_data():
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1, rtscts=True, dsrdtr=True, write_timeout=0)
        time.sleep(2)  # Wait for connection to stabilize
        
        print("Starting data collection...")
        scan_count = 0
        
        while scan_count < TOTAL_SCANS:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line == '9999':  # Start marker
                    i = 0
                    print(f"Scan {scan_count+1}/{TOTAL_SCANS} in progress...")
                    
                    while i < 90:
                        line = ser.readline().decode('utf-8').strip()
                        if line == '-9999':  # End marker
                            break
                        elif line.isdigit() or (line.startswith('-') and line[1:].isdigit()):
                            data[i].append(int(line))
                            time.sleep(0.01)  # Small delay
                        else:
                            i -= 1
                        i += 1
                    
                    scan_count += 1
                    print(f"Scan {scan_count}/{TOTAL_SCANS} completed")
        
        ser.close()
        print("Data collection completed!")
        return True
        
    except Exception as e:
        print(f"Serial communication error: {e}")
        return False

# Function to save data to file
def save_to_file(filename="scan_data.txt"):
    try:
        with open(filename, 'w') as f:
            f.write(f"# Scan data - {TOTAL_SCANS} scans\n")
            f.write("# Format: angle, value1, value2, ..., valueN\n")
            
            angles = np.linspace(0, 270, 90)
            for i in range(90):
                # Write angle followed by all values
                f.write(f"{angles[i]:.1f}")
                for value in data[i]:
                    f.write(f",{value}")
                f.write("\n")
                
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

if __name__ == "__main__":
    if collect_data():
        save_to_file()