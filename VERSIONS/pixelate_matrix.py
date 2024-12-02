from PIL import Image
import numpy as np
import serial
import time

# Configuration variables
GROUP_SIZE = 4        # Number of pixels per group
TARGET_WIDTH = 20     # Width of the image in pixels
SERIAL_PORT = '/dev/cu.usbmodem1401'
BAUD_RATE = 9600
DELAY_SECONDS = 10    # Delay between rows

def analyze_binary_image(image_path, output_path):
    # Initialize serial connection
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for serial connection to establish
    
    NUM_GROUPS = TARGET_WIDTH // GROUP_SIZE
    
    # resize
    img = Image.open(image_path).convert('L')
    width_percent = TARGET_WIDTH / float(img.size[0])
    target_height = int(float(img.size[1]) * width_percent)
    resized = img.resize((TARGET_WIDTH, target_height), Image.NEAREST)
    
    # binary
    binary = np.array(resized) > 127
    binary_image = Image.fromarray(binary.astype(np.uint8) * 255)
    binary_image.save(output_path)
     
    row_counts = []
    pixel_lists = []
    expanded_lists = []
    group_numbers = []
    
    for row in binary:
        # row to integers
        row_ints = row.astype(int).tolist()
        pixel_lists.append(row_ints)
        
        # Count black and white
        black_pixels = np.sum(row == 0)
        white_pixels = np.sum(row == 1)
        row_counts.append((black_pixels, white_pixels))
        
        # Compressed representation
        compressed_row = []
        for i in range(0, len(row), GROUP_SIZE):
            group = row_ints[i:i+GROUP_SIZE]
            compressed_row.append(1 if sum(group) > len(group)/2 else 0)
        
        # expanded representation
        expanded_row = []
        for value in compressed_row:
            expanded_row.extend([value] * GROUP_SIZE)
        expanded_lists.append(expanded_row)
        
        # Create group number representation and send to serial
        row_binary = ''.join(str(value) for value in compressed_row)
        print(f"Sending row: {row_binary}")
        ser.write(f"{row_binary}\n".encode())  # Send row with newline
        time.sleep(DELAY_SECONDS)  # Wait before sending next row
        print(f"Waiting {DELAY_SECONDS} seconds untill next row")
        group_numbers.append(compressed_row)

    # Close serial connection
    ser.close()
    
    return binary, row_counts, expanded_lists, group_numbers

try:
    binary_array, counts, expanded, groups = analyze_binary_image("duck.png", "output.png")
except serial.SerialException as e:
    print(f"Error: Could not open serial port {SERIAL_PORT}. Make sure it's connected and the port name is correct.")
    print(f"Error details: {e}")
except Exception as e:
    print(f"An error occurred: {e}")