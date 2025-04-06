def solve_nonogram(col_clues, row_clues, size_m):
    # Generate all possible patterns for each row
    def generate_row_patterns(clue, length):
        if not clue:
            return [[0] * length]
        if clue == [0]:
            return [[0] * length]
        
        patterns = []
        total_blocks = sum(clue) + len(clue) - 1
        
        if total_blocks > length:
            return []
        
        def backtrack(current, block_idx, pos):
            if block_idx == len(clue):
                if len(current) == length:
                    patterns.append(current.copy())
                elif len(current) < length:
                    patterns.append(current + [0] * (length - len(current)))
                return
            
            block_len = clue[block_idx]
            remaining_blocks = sum(clue[block_idx+1:]) + len(clue[block_idx+1:])
            max_pos = length - remaining_blocks - block_len
            
            for p in range(pos, max_pos + 1):
                new_current = current + [0] * (p - len(current)) + [1] * block_len
                if block_idx < len(clue) - 1:
                    new_current.append(0)  # mandatory space between blocks
                backtrack(new_current, block_idx + 1, p + block_len + 1)
        
        backtrack([], 0, 0)
        return patterns

    # Generate all possible patterns for each row
    row_patterns = [generate_row_patterns(clue, size_m) for clue in row_clues]
    
    # Check if current grid satisfies column clues
    def is_valid(grid):
        for col_idx in range(size_m):
            col = [grid[row_idx][col_idx] for row_idx in range(size_m)]
            runs = []
            current = 0
            for cell in col:
                if cell == 1:
                    current += 1
                elif current > 0:
                    runs.append(current)
                    current = 0
            if current > 0:
                runs.append(current)
            if runs != col_clues[col_idx]:
                return False
        return True

    solution = []
    game_states = [0]  # Using list to allow modification in nested functions

    def backtrack(row_idx, grid):
        if row_idx == size_m:
            if is_valid(grid):
                print(grid)
                nonlocal solution
                solution = [row.copy() for row in grid]
                return True
            return False
        print(grid)
        
        for pattern in row_patterns[row_idx]:
            new_grid = [row.copy() for row in grid]
            new_grid[row_idx] = pattern
            game_states[0] += 1
            
            # Check column constraints up to current row
            valid = True
            for col_idx in range(size_m):
                col_so_far = [new_grid[i][col_idx] for i in range(row_idx + 1)]
                runs = []
                current = 0
                for cell in col_so_far:
                    if cell == 1:
                        current += 1
                    elif current > 0:
                        runs.append(current)
                        current = 0
                if current > 0:
                    runs.append(current)
                
                # Check if runs match the beginning of column clue
                col_clue = col_clues[col_idx]
                if len(runs) > len(col_clue):
                    valid = False
                    break
                for i in range(len(runs)):
                    if runs[i] != col_clue[i]:
                        valid = False
                        break
                # Check if we have enough remaining cells for remaining blocks
                remaining_cells = size_m - (row_idx + 1)
                remaining_blocks = sum(col_clue[len(runs):]) + max(0, len(col_clue[len(runs):]) - 1)
                if remaining_blocks > remaining_cells:
                    valid = False
                    break
            
            if valid and backtrack(row_idx + 1, new_grid):
                return True
        
        return False

    initial_grid = [[0 for _ in range(size_m)] for _ in range(size_m)]
    backtrack(0, initial_grid)
    return solution, game_states[0]

# Given clues
column_clues = [[1], [2], [2], [2]]
row_clues = [[1], [1, 1], [2], [2]]
m = 4

solution, num_game_states = solve_nonogram(column_clues, row_clues, m)

if solution:
    print("Number of game states explored:", num_game_states)
    print("Solution:")
    for row in solution:
        print(' '.join('#' if x == 1 else '.' for x in row))
else:
    print("No solution exists for the given clues.")