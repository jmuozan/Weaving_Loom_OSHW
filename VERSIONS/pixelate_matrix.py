from PIL import Image
import numpy as np

# Configuration variables
GROUP_SIZE = 4        # Number of pixels per group
TARGET_WIDTH = 20     # Width of the image in pixels

def analyze_binary_image(image_path, output_path):
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
        
        # Create group number representation (1-based numbering)
        group_row = []
        for i, value in enumerate(compressed_row, 1):
            #group_row.append(f"G{i}:{value}")
            group_row.append(f"{value}")
        group_numbers.append(group_row)
    '''
    print(f"\nImage configuration:")
    print(f"Width: {TARGET_WIDTH} pixels")
    print(f"Group size: {GROUP_SIZE} pixels")
    print(f"Number of groups per row: {NUM_GROUPS}")
    '''
    print("\nSimplified group representation (Group:Value):")
    for i, row in enumerate(group_numbers):
        print(f"Row {i+1}: {row}")
        
    print("\nFull binary representation (0=black, 1=white):")
    for i, row in enumerate(expanded_lists):
        print(f"Row {i+1}: {row}")

    return binary, row_counts, expanded_lists, group_numbers

binary_array, counts, expanded, groups = analyze_binary_image("input.jpg", "output.png")