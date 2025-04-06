from itertools import combinations, product

def generate_row_combinations(row_clue, size):
    if row_clue == [0]:  # Special case: fully empty row
        return [['_'] * size]
    
    total_blocks = sum(row_clue)
    num_gaps = len(row_clue) - 1
    total_empty = size - total_blocks - num_gaps

    results = []

    def backtrack(idx, pos, row):
        if idx == len(row_clue):
            results.append(row[:])
            return

        block_size = row_clue[idx]
        for i in range(pos, size - block_size + 1):
            # Check if enough space is left
            if any(cell == '#' for cell in row[i:i+block_size]):
                continue
            if idx > 0 and row[i - 1] != '_':
                continue
            new_row = row[:]
            new_row[i:i + block_size] = ['#'] * block_size
            if i + block_size < size:
                new_row[i + block_size] = '_'
            backtrack(idx + 1, i + block_size + 1, new_row)

    row = ['_'] * size
    backtrack(0, 0, row)
    return results

def generate_all_row_combinations(row_clues, size):
    return {i: generate_row_combinations(row_clue, size) for i, row_clue in enumerate(row_clues)}

def extract_column_clues(grid):
    num_cols = len(grid[0])
    column_clues = []

    for col_idx in range(num_cols):
        col = [grid[row_idx][col_idx] for row_idx in range(len(grid))]
        clues = []
        count = 0

        for cell in col:
            if cell == '#':
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0

        if count > 0:
            clues.append(count)

        column_clues.append(clues if clues else [0])

    return column_clues

def grid_matches_column_clues(grid, column_clues):
    return extract_column_clues(grid) == column_clues

def generate_valid_grids(row_combinations, column_clues):
    all_possible_rows = [row_combinations[i] for i in range(len(row_combinations))]
    
    valid_grids = []
    total_states = 0

    for grid in product(*all_possible_rows):
        total_states += 1
        if grid_matches_column_clues(grid, column_clues):
            valid_grids.append(grid)

    return valid_grids, total_states

def print_grid_count_and_grids(valid_grids, total_states):
    print(f"Total possible states: {total_states}")
    print(f"Valid grids: {len(valid_grids)}")
    print("\nValid grids:")
    for grid in valid_grids:
        for row in grid:
            print(''.join(row))
        print(' ' * len(grid[0]))

# Example Usage
column_clues = [[2], [2], [1,1], [1]]
row_clues = [[1], [0], [4], [2]]
column_clues = [[1], [2], [2], [2]]
row_clues = [[1], [1,1], [2], [2]]
# row_clues = [[2], [4], [1, 1], [1], [2], [1]]
# column_clues = [[2], [1], [2, 1], [5], [1], [0]]
# column_clues = [[2],[1,3],[1,1,3],[2,7],[4,3],[2,4],[3,1],[2,1,1],[1,3],[1,1,3]]
# row_clues = [[3,1,1],[6],[1,1,2],[6],[1,1],[1,5],[1,1,2],[4,3],[5],[5]]


size = 4

row_combinations = generate_all_row_combinations(row_clues, size)

valid_grids, total_states = generate_valid_grids(row_combinations, column_clues)

print_grid_count_and_grids(valid_grids, total_states)
