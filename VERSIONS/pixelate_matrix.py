from PIL import Image
import numpy as np

def analyze_binary_image(image_path, target_width, output_path):
    img = Image.open(image_path).convert('L')
    width_percent = target_width / float(img.size[0])
    target_height = int(float(img.size[1]) * width_percent)
    resized = img.resize((target_width, target_height), Image.NEAREST)
    
    binary = np.array(resized) > 127
    binary_image = Image.fromarray(binary.astype(np.uint8) * 255)
    binary_image.save(output_path)
    
    row_counts = []
    pixel_lists = []
    
    for row in binary:
        black_pixels = np.sum(row == 0)
        white_pixels = np.sum(row == 1)
        row_counts.append((black_pixels, white_pixels))
        pixel_lists.append(row.astype(int).tolist())
    
    print("\nPixel counts per row (Black, White):")
    for i, (black, white) in enumerate(row_counts):
        print(f"Row {i+1}: {black} black, {white} white")
    
    print("\nBinary representation of each row (0=black, 1=white):") 
    for i, row in enumerate(pixel_lists):
        print(f"Row {i+1}: {row}")
    
    return binary, row_counts, pixel_lists

# Usage:
binary_array, counts, lists = analyze_binary_image("input.jpg", 8, "output.png")