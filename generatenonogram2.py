import random
import csv
from typing import List
from calculate_states import calculate_row_states

def generate_clue(line: List[str]) -> List[int]:
    """
    Given a list of cells (each either '#' or '_'),
    return the Nonogram clue (consecutive '#' counts).
    """
    clues = []
    count = 0
    for cell in line:
        if cell == '#':
            count += 1
        else:
            if count > 0:
                clues.append(count)
                count = 0
    # If the last cells were '#', append the final count
    if count > 0:
        clues.append(count)
    # If no filled cells, return [0]
    return clues if clues else [0]


def generate_nonogram(size=4):
    """
    Create a random grid of '#' and '_' of given size,
    then generate row and column clues. Return the CSV-like data
    plus the row and column clues as lists of ints.
    
    Column clues must contain only one number (i.e., one contiguous block).
    """
    while True:
        # Create a random grid
        grid = [[random.choice(['#', '_']) for _ in range(size)] for _ in range(size)]
        
        # Generate row clues
        row_clues = [generate_clue(row) for row in grid]
        
        # Generate column clues
        column_clues = []
        valid = True
        for col in range(size):
            column = [grid[r][col] for r in range(size)]
            clue = generate_clue(column)
            if len(clue) != 1:  # Ensure each column has only one contiguous block
                valid = False
                break
            column_clues.append(clue)
        
        # Retry if any column clue has more than one number
        if not valid:
            continue
        
        # Prepare data for CSV
        column_clues_str = [str(clue).replace(' ', '') for clue in column_clues]
        
        # First row of CSV: the column clues
        data = [['Clue'] + column_clues_str]
        
        # Subsequent rows: row clue + the actual grid
        for i in range(size):
            data.append([str(row_clues[i]).replace(' ', '')] + grid[i])
        
        return data, row_clues, column_clues

def calculate_min_state(row_clues: List[List[int]], column_clues: List[List[int]], size: int) -> int:
    """
    Calculate the "min_state" as the minimum of the product of
    valid row states and valid column states.
    """
    row_states = 1
    col_states = 1

    for row in row_clues:
        row_states *= calculate_row_states(row, size)
    for col in column_clues:
        col_states *= calculate_row_states(col, size)

    return max(row_states, col_states)


def generate_valid_nonogram(size=4):
    """
    Keep generating random 4x4 Nonograms until the min_state is between 90 and 120.
    Return the CSV-like data once we get a puzzle in that range.
    """
    min_state = float('inf')
    while min_state > 120 or min_state < 90:
        nonogram_data, row_clues, column_clues = generate_nonogram(size)
        min_state = calculate_min_state(row_clues, column_clues, size)
        print(f"Generated nonogram with min_state: {min_state}")
    return nonogram_data


def replace_shaded_squares(input_filename: str, output_filename: str):
    """
    Read a CSV, replace all '#' with '_', and save to a new file.
    This creates the 'problem' version from the 'solution' version.
    """
    with open(input_filename, mode='r', newline='') as infile:
        reader = csv.reader(infile)
        data = []
        for row in reader:
            new_row = []
            for cell in row:
                new_row.append(cell.replace('#', '_'))
            data.append(new_row)
    
    with open(output_filename, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)
    
    print(f"All '#' replaced with '_' and saved to {output_filename}")


if __name__ == "__main__":
    # Generate a valid nonogram and save it
    valid_nonogram_data = generate_valid_nonogram(size=4)

    solution_filename = './4x4_nonogram_solo_solution.csv'
    with open(solution_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(valid_nonogram_data)

    # Create a 'problem' version (with all '#' replaced by '_')
    replace_shaded_squares(solution_filename, f'4x4_nonogram_solo_problem.csv')

    print("Valid 4x4 Nonogram has been generated in CSV format!")
