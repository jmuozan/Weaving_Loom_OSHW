from PIL import Image
import numpy as np
import serial
import time

def analyze_and_transmit(image_path, target_width, output_path, serial_port, baudrate=9600):
    try:
        SerialObj = serial.Serial(serial_port)
        SerialObj.baudrate = baudrate
        SerialObj.bytesize = 8
        SerialObj.parity = 'N'
        SerialObj.stopbits = 1
        time.sleep(3)
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

    try:
        img = Image.open(image_path).convert('L')
        width_percent = target_width / float(img.size[0])
        target_height = int(float(img.size[1]) * width_percent)
        resized = img.resize((target_width, target_height), Image.NEAREST)
        binary = np.array(resized) > 127
        binary_image = Image.fromarray(binary.astype(np.uint8) * 255)
        binary_image.save(output_path)

        print("\nAnalyzing and transmitting row data:")
        total_rows = len(binary)
        for i, row in enumerate(binary):
            white_count = np.sum(row == 1)
            black_count = np.sum(row == 0)
            dominant_color = 1 if white_count > black_count else 0
            print(f"Processing Row {i+1} of {total_rows}: Dominant color = {dominant_color}")
            print(f"Progress: {((i+1)/total_rows)*100:.1f}%")
            SerialObj.write(str(dominant_color).encode())
            
            # Wait time between rows
            if i < total_rows - 1:
                print(f"Waiting 20 seconds before processing next row...")
                time.sleep(5)
        
        # Add final wait before closing
        print("Processing complete. Waiting 20 seconds before closing...")
        time.sleep(5)
        print("-" * 50)

    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        SerialObj.close()
        print("\nSerial connection closed")

if __name__ == "__main__":
    analyze_and_transmit(
        image_path="input.png",
        target_width=5,
        output_path="output.png",
        serial_port='/dev/cu.usbmodem1301'
    )