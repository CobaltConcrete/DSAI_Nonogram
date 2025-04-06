from itertools import product
from typing import List

def generate_row_combinations(clue: List[int], size: int) -> List[List[str]]:
    if clue == [0]:
        return [['_'] * size]
    
    total_blocks = sum(clue)
    gaps = len(clue) - 1
    total_empty = size - total_blocks - gaps

    results = []

    def backtrack(idx, pos, row):
        if idx == len(clue):
            results.append(row[:])
            return
        
        block = clue[idx]
        for i in range(pos, size - block + 1):
            if any(cell == '#' for cell in row[i:i+block]):
                continue
            if i > 0 and row[i-1] == '#':
                continue
            new_row = row[:]
            new_row[i:i+block] = ['#'] * block
            if i + block < size:
                new_row[i+block] = '_'
            backtrack(idx + 1, i + block + 1, new_row)

    backtrack(0, 0, ['_'] * size)
    return results

def solve_nonogram(m: int, row_clues: List[List[int]], col_clues: List[List[int]]):
    row_options = [generate_row_combinations(clue, m) for clue in row_clues]
    col_targets = [sum(clue) for clue in col_clues]
    solutions = []
    game_state_counter = 0

    def backtrack(grid: List[List[str]], row: int, col_counts: List[int]):
        nonlocal game_state_counter

        if row == m:
            # All rows placed, check if final column counts match the clues
            for j in range(m):
                if generate_clue([grid[i][j] for i in range(m)]) != col_clues[j]:
                    return
            solutions.append([row[:] for row in grid])
            return

        for option in row_options[row]:
            new_col_counts = col_counts[:]
            valid = True

            for j in range(m):
                if option[j] == '#':
                    new_col_counts[j] += 1
                    # Condition 1: Too many shaded cells
                    if new_col_counts[j] > col_targets[j]:
                        valid = False
                        break
                    # Condition 2: Not enough space left
                    remaining_rows = m - row - 1
                    if remaining_rows < col_targets[j] - new_col_counts[j]:
                        valid = False
                        break

            if not valid:
                continue

            game_state_counter += 1
            backtrack(grid + [option], row + 1, new_col_counts)

    backtrack([], 0, [0] * m)

    return solutions, game_state_counter

def generate_clue(line: List[str]) -> List[int]:
    clues = []
    count = 0
    for cell in line:
        if cell == '#':
            count += 1
        else:
            if count > 0:
                clues.append(count)
                count = 0
    if count > 0:
        clues.append(count)
    return clues if clues else [0]

# Example usage
m = 4
col_clues = [[1], [2], [2], [2]]
row_clues = [[1], [1, 1], [2], [2]]

solutions, game_states = solve_nonogram(m, row_clues, col_clues)

print(f"Total game states processed: {game_states}")
print(f"Number of valid solutions: {len(solutions)}\n")

for sol_num, grid in enumerate(solutions, 1):
    print(f"Solution {sol_num}:")
    for row in grid:
        print(''.join(row))
    print("-" * m)
