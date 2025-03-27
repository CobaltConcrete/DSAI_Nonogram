import csv
from PIL import Image, ImageDraw, ImageFont

# Function to convert CSV nonogram data into a visible PNG with clues
def convert_nonogram_to_png(input_csv_path, output_image_path, is_solution, cell_size=40):
    # Read CSV data
    with open(input_csv_path, mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Extract the clues from the CSV data
    grid = [row[1:] for row in rows[1:]]  # Skipping the 'Clue' row

    # Extract row and column clues
    row_clues = [row[0] for row in rows[1:]]
    column_clues = list(zip(*grid))  # Transpose to get column clues
    
    # Create a new image with a white background
    num_rows = len(grid)
    num_cols = len(grid[0])
    
    # Adding space for clues on the left side: We reserve space for the row clues and column clues
    img_width = (num_cols + 1) * cell_size + 100  # Extra space for column clues and buffer on the right
    img_height = (num_rows + 1) * cell_size + 20  # Reduced space at the bottom for row clues
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Set up font for clues (if available, or default)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Indentation offsets
    row_clue_offset = 10  # Indentation for row clues
    col_clue_offset = 10  # Indentation for column clues (added space on the left side)

    # Draw the grid and clues
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            x1 = col_idx * cell_size + 40 + 80  # X coordinate for cell's left edge
            y1 = row_idx * cell_size + 40  # Y coordinate for cell's top edge
            x2 = (col_idx + 1) * cell_size + 40 + 80  # X coordinate for cell's right edge
            y2 = (row_idx + 1) * cell_size + 40  # Y coordinate for cell's bottom edge

            if is_solution:
                if cell == "#":
                    # Draw a shaded square
                    draw.rectangle([x1, y1, x2, y2], fill="black")
                elif cell == "_":
                    # Draw a white cell with black borders
                    draw.rectangle([x1, y1, x2, y2], outline="black", fill="white")
            else:
                draw.rectangle([x1, y1, x2, y2], outline="black", fill="white")
        
        # Draw row clues to the left of each row (with indentation)
        draw.text((20, row_idx * cell_size + 50), str(row_clues[row_idx]), fill="black", font=font)

    # Draw column clues above each column (with indentation)
    for col_idx, clue in enumerate(column_clues):
        draw.text((col_idx * cell_size + 40 + col_clue_offset + 80, 10), str([clue.count('#')]), fill="black", font=font)

    # Save the image to a file
    img.save(output_image_path)
    print(f"Image saved as {output_image_path}")

# Example Usage
input_csv_path = "./5x5_nonogram_solution.csv"  # Specify your input CSV file path here
output_image_path = "nonogram_solution_output.png"
# Convert the nonogram into a PNG with row and column clues
convert_nonogram_to_png(input_csv_path, output_image_path, True)
convert_nonogram_to_png(input_csv_path, "nonogram_problem_output.png", False)