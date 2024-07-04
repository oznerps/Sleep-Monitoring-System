import serial
import csv
import time
from datetime import datetime

# Set up the serial port (adjust 'COM3' to your specific port)
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Open CSV file to save the data
with open('sleep_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Event', 'Start Time (Minutes)', 'End Time(Minutes)', 'Duration (seconds)'])  # Write CSV header

    motion_start = None
    motion_end = None

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # Read data from serial port
            if line:
                current_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Use consistent time format
                
                if line.startswith("Motion detected"):
                    if motion_start is None:
                        motion_start = current_time
                    if motion_end:
                        idle_duration = (datetime.strptime(current_time, '%H:%M:%S.%f') - datetime.strptime(motion_end, '%H:%M:%S.%f')).total_seconds()
                        csvwriter.writerow(["Idle", motion_end, current_time, idle_duration])
                        motion_end = None

                elif line.startswith("Motion ended"):
                    if motion_start:
                        motion_end = current_time
                        motion_duration = (datetime.strptime(motion_end, '%H:%M:%S.%f') - datetime.strptime(motion_start, '%H:%M:%S.%f')).total_seconds()
                        csvwriter.writerow(["Motion", motion_start, motion_end, motion_duration])
                        motion_start = None

                print(f"{line} at {current_time}")

    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        ser.close()  # Close the serial port
