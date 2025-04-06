from itertools import product
from itertools import groupby
from collections import deque

def is_valid_line(line, clues):
    """Check if a line (row or column) satisfies the given clues."""
    blocks = [len(list(g)) for k, g in groupby(line) if k == 1]
    return blocks == clues

def solve_nonogram_bfs(column_clues, row_clues):
    rows, cols = len(row_clues), len(column_clues)
    grid = [[-1] * cols for _ in range(rows)]  # -1 represents an unknown cell
    states_explored = 0
    
    queue = deque([(grid, 0, 0)])  # (current grid, row index, col index)
    
    def is_valid(grid):
        """Check if the current grid satisfies all filled rows and columns."""
        for r in range(rows):
            if -1 not in grid[r] and not is_valid_line(grid[r], row_clues[r]):
                return False
        for c in range(cols):
            col = [grid[r][c] for r in range(rows)]
            if -1 not in col and not is_valid_line(col, column_clues[c]):
                return False
        return True
    
    while queue:
        grid, r, c = queue.popleft()
        states_explored += 1
        
        if r == rows:
            if is_valid(grid):
                return grid, states_explored
            continue
        
        next_r, next_c = (r, c + 1) if c + 1 < cols else (r + 1, 0)
        
        for val in (0, 1):
            new_grid = [row[:] for row in grid]  # Copy grid
            new_grid[r][c] = val
            if is_valid(new_grid):
                queue.append((new_grid, next_r, next_c))
    
    return None, states_explored  # No solution found

# column_clues = [[1,1,1],[2,1],[3],[2],[2,1]]
# row_clues = [[3,1],[2,1],[1,1],[1,2],[1,1]]
column_clues = [[2],[3],[1,1],[0]]
row_clues = [[1],[1],[2],[3]]

solution, states_explored = solve_nonogram_bfs(column_clues, row_clues)
print("Solution:")
if solution:
    for row in solution:
        print("".join("#" if cell == 1 else "_" for cell in row))
else:
    print("No solution found")
print("Game states explored:", states_explored)
