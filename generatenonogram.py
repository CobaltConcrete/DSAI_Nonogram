import random
import csv
from math import comb
from typing import List

# Function to calculate valid states for a given row or column
def calculate_states(clue: List[int], max_cells: int) -> int:
    """
    Calculate the number of valid ways to place a given Nonogram row clue within a row of max_cells.

    :param clue: List of integers representing the clue (block sizes).
    :param max_cells: The total number of cells in the row.
    :return: The number of valid configurations for the given clue in the row.
    """
    # If the clue contains only [0], it means no shaded blocks, so return 0
    if clue == [0]:
        return 0
    
    w = len(clue)  # Number of groups
    occupied_space = sum(clue)  # Sum of filled cells
    min_required_space = occupied_space + (w - 1)  # Including mandatory gaps
    
    # If the total required space exceeds max_cells, return 0 (impossible case)
    if min_required_space > max_cells:
        return 0

    # Remaining free spaces available for distribution
    free_spaces = max_cells - min_required_space

    # Compute the number of ways to distribute free spaces using combinations formula
    return comb(free_spaces + w, w)

# Function to generate a random 5x5 nonogram with row and column clues
def generate_nonogram(size=5):
    # Create a random grid with # (shaded) and X (blank)
    grid = [[random.choice(['#', '_']) for _ in range(size)] for _ in range(size)]
    
    # Function to generate clues for a line (row or column)
    def generate_clue(line):
        clues = []
        count = 0
        for cell in line:
            if cell == '#':  # Shaded square
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        return clues if clues else [0]
    
    # Generate row and column clues
    row_clues = [generate_clue(row) for row in grid]
    column_clues = [generate_clue([grid[row][col] for row in range(size)]) for col in range(size)]
    
    # Convert column clues to the required format (list of integers)
    column_clues_str = [str(clue).replace(' ', '') for clue in column_clues]

    # Prepare data to write in CSV format
    data = [['Clue'] + column_clues_str]
    for i in range(size):
        data.append([str(row_clues[i]).replace(' ', '')] + grid[i])

    return data, row_clues, column_clues

# Function to calculate the min state based on row and column states
def calculate_min_state(row_clues, column_clues, size):
    row_states = 1
    col_states = 1
    
    # Calculate row states
    for row in row_clues:
        row_states *= calculate_states(row, size)
    
    # Calculate column states
    for col in column_clues:
        col_states *= calculate_states(col, size)
    
    # Return the minimum of row and column states
    return min(row_states, col_states)

# Keep generating nonograms until the minimum state is <= 120
def generate_valid_nonogram(size=5):
    min_state = float('inf')
    while min_state > 120 or min_state < 90:
        nonogram_data, row_clues, column_clues = generate_nonogram(size)
        min_state = calculate_min_state(row_clues, column_clues, size)
        print(f"Generated nonogram with min_state: {min_state}")
    return nonogram_data

def replace_shaded_squares(input_filename, output_filename):
    with open(input_filename, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = [ [cell.replace('#', '_') for cell in row] for row in reader ]
    
    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)

    print(f"All '#' replaced with '_' and saved to {output_filename}")

# Generate a valid nonogram
valid_nonogram_data = generate_valid_nonogram()

# Write the nonogram to CSV
solution_filename = './5x5_nonogram_solution.csv'
with open(solution_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(valid_nonogram_data)
replace_shaded_squares(solution_filename, '5x5_nonogram_problem.csv')

print("Valid 5x5 Nonogram has been generated in CSV format!")
