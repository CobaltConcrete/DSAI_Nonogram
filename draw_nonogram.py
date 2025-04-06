import csv
from PIL import Image, ImageDraw, ImageFont

def convert_nonogram_to_png(input_csv_path: str,
                            output_image_path: str,
                            is_solution: bool,
                            cell_size: int = 40):
    """
    Convert the CSV nonogram data into a PNG image.
    If 'is_solution' is True, '#' cells are filled black.
    Otherwise, all cells are left white.
    Row and column clues are taken directly from the CSV.
    """
    # Read CSV data
    with open(input_csv_path, mode="r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # The first row has the format: ['Clue', 'col_clue1', 'col_clue2', ...]
    column_clues = rows[0][1:]  # skip 'Clue'
    
    # The subsequent rows each have:
    # row[0] -> row clue (e.g. '[2,1]')
    # row[1:] -> the actual row cells (e.g. ['#','_','#','_','_'])
    row_clues = []
    grid = []
    for r in rows[1:]:
        row_clues.append(r[0])       # e.g. '[1,1]'
        grid.append(r[1:])          # e.g. ['#','_','#','_','_']

    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    # Margins
    left_margin = 80
    top_margin = 60
    bottom_margin = 20
    right_margin = 20

    # Image dimensions
    img_width = left_margin + (num_cols * cell_size) + right_margin
    img_height = top_margin + (num_rows * cell_size) + bottom_margin

    # Create a new image with a white background
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Try loading a TrueType font; fallback to default if not found
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # Draw the grid
    for row_idx in range(num_rows):
        for col_idx in range(num_cols):
            x1 = left_margin + col_idx * cell_size
            y1 = top_margin + row_idx * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            if is_solution and grid[row_idx][col_idx] == '#':
                # Filled (solution)
                draw.rectangle([x1, y1, x2, y2], fill="black")
            else:
                # Empty cell
                draw.rectangle([x1, y1, x2, y2], outline="black", fill="white")

    # Draw row clues on the left
    for row_idx in range(num_rows):
        clue_text = row_clues[row_idx]  # e.g. '[2,1]'
        text_x = left_margin - 50
        text_y = top_margin + row_idx * cell_size + (cell_size // 4)
        draw.text((text_x, text_y), clue_text, fill="black", font=font)

    # Draw column clues above each column
    for col_idx in range(num_cols):
        clue_text = column_clues[col_idx]  # e.g. '[2,1]'
        text_x = left_margin + col_idx * cell_size + (cell_size // 4)
        text_y = top_margin - 30
        draw.text((text_x, text_y), clue_text, fill="black", font=font)

    # Save the image
    img.save(output_image_path)
    print(f"Image saved as {output_image_path}")


if __name__ == "__main__":
    # Example usage
    input_csv_path = "./4x4_nonogram_solution.csv"
    solution_image_path = "4x4_nonogram_solution_output.png"
    problem_image_path = "4x4_nonogram_problem_output.png"

    # Draw the solution version (filled cells)
    convert_nonogram_to_png(input_csv_path, solution_image_path, is_solution=True)

    # Draw a 'blank' version (problem)
    convert_nonogram_to_png(input_csv_path, problem_image_path, is_solution=False)
