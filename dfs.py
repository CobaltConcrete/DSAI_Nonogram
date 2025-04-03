from itertools import product

def is_valid_line(line, clues):
    """Check if a line (row or column) satisfies the given clues."""
    blocks = [len(list(g)) for k, g in groupby(line) if k == 1]
    return blocks == clues

from itertools import product
from itertools import groupby

def solve_nonogram(column_clues, row_clues):
    rows, cols = len(row_clues), len(column_clues)
    grid = [[-1] * cols for _ in range(rows)]  # -1 represents an unknown cell
    states_explored = 0
    
    def is_valid():
        """Check if the current grid satisfies all filled rows and columns."""
        for r in range(rows):
            if -1 not in grid[r] and not is_valid_line(grid[r], row_clues[r]):
                return False
        for c in range(cols):
            col = [grid[r][c] for r in range(rows)]
            if -1 not in col and not is_valid_line(col, column_clues[c]):
                return False
        return True
    
    def dfs(r, c):
        nonlocal states_explored
        if r == rows:
            return is_valid()
        
        next_r, next_c = (r, c + 1) if c + 1 < cols else (r + 1, 0)
        for val in (0, 1):  # Try empty (0) or filled (1)
            grid[r][c] = val
            states_explored += 1
            if is_valid() and dfs(next_r, next_c):
                return True
        grid[r][c] = -1  # Backtrack
        return False
    
    dfs(0, 0)
    return grid, states_explored

column_clues = [[1,1,1],[2,1],[3],[2],[2,1]]
row_clues = [[3,1],[2,1],[1,1],[1,2],[1,1]]

solution, states_explored = solve_nonogram(column_clues, row_clues)
print("Solution:")
for row in solution:
    print("".join("#" if cell == 1 else "." for cell in row))
print("Game states explored:", states_explored)
