from PIL import Image
import numpy as np

def analyze_row_dominance(image_path, target_width, output_path):
    # Load and process image
    img = Image.open(image_path).convert('L')
    width_percent = target_width / float(img.size[0])
    target_height = int(float(img.size[1]) * width_percent)
    resized = img.resize((target_width, target_height), Image.NEAREST)
    
    binary = np.array(resized) > 127
    binary_image = Image.fromarray(binary.astype(np.uint8) * 255)
    binary_image.save(output_path)
    
    # Determine dominant color per row (0=black dominant, 1=white dominant)
    dominant_colors = []
    for row in binary:
        white_count = np.sum(row == 1)
        black_count = np.sum(row == 0)
        dominant_colors.append(1 if white_count > black_count else 0)
    
    # Print results
    print("\nDominant color per row (0=black dominant, 1=white dominant):")
    for i, color in enumerate(dominant_colors):
        print(f"Row {i+1}: {color}")
    
    return dominant_colors

# Usage:
dominant_colors = analyze_row_dominance("input.jpg", 10, "output.png")