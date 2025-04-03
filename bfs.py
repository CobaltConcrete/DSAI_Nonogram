import copy
from collections import deque

# ---------------------------
# Helper functions and classes
# ---------------------------

def get_pattern(line):
    """
    Given a list (row or column) with values 0, 1, or -1, return the list of filled groups.
    For example, [1, 1, 0, 1, 0] returns [2, 1].
    """
    pattern = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        else:
            if count > 0:
                pattern.append(count)
                count = 0
    if count > 0:
        pattern.append(count)
    return pattern

def valid_line(line, clue):
    """
    Check if a given line (row or column) is valid with respect to its clue.
    - If the line is complete (no -1), the pattern must match the clue exactly.
    - For a partial line, the filled groups so far must be a valid prefix of the clue.
    """
    pattern = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        else:
            if count > 0:
                pattern.append(count)
                count = 0
    if count > 0:
        pattern.append(count)
    
    # If the line is complete, the pattern must match the clue exactly.
    if -1 not in line:
        return pattern == clue
    
    # For a partial line, pattern must be a prefix of the clue.
    if len(pattern) > len(clue):
        return False
    for i in range(len(pattern)):
        if pattern[i] > clue[i]:
            return False
    return True

def board_to_tuple(board):
    """Convert board (list of lists) to a tuple of tuples for hashing."""
    return tuple(tuple(row) for row in board)

def render_board(board):
    """Prints the board in a simple text-based format."""
    for row in board:
        print(" ".join(str(cell) if cell != -1 else '.' for cell in row))
    print()

class NonogramState:
    def __init__(self, board, index=0, cost=0, parent=None):
        self.board = board      # 2D list representing the board
        self.index = index      # Next cell index (row-major order) to fill
        self.cost = cost        # Cost so far (each move costs 1)
        self.parent = parent    # For reconstructing the solution path (if needed)
    
    def __lt__(self, other):
        # For any potential priority queue usage (not used in BFS)
        return self.cost < other.cost

def is_valid_state(state, row_clues, col_clues):
    n = len(state.board)
    # Check each row
    for i in range(n):
        if not valid_line(state.board[i], row_clues[i]):
            return False
    # Check each column
    for j in range(n):
        col = [state.board[i][j] for i in range(n)]
        if not valid_line(col, col_clues[j]):
            return False
    return True

def is_goal(state, row_clues, col_clues):
    """A goal state is reached if there are no undecided cells and the state is valid."""
    n = len(state.board)
    for i in range(n):
        if -1 in state.board[i]:
            return False
    return is_valid_state(state, row_clues, col_clues)

def get_successors(state, n):
    """
    Expand the state by assigning the next undecided cell either 0 (empty) or 1 (filled).
    """
    if state.index >= n * n:
        return []
    i = state.index // n
    j = state.index % n
    successors = []
    for val in [0, 1]:
        new_board = copy.deepcopy(state.board)
        new_board[i][j] = val
        new_state = NonogramState(new_board, state.index + 1, state.cost + 1, parent=state)
        successors.append(new_state)
    return successors

# ---------------------------
# Breadth First Search Function
# ---------------------------
def search_bfs(initial_state, row_clues, col_clues, n):
    """
    Breadth-first search (BFS) for Nonogram.
    Returns a tuple: (solution_state, number_of_game_states_reached)
    """
    frontier = deque([initial_state])
    visited = set()
    nodes_expanded = 0
    
    while frontier:
        state = frontier.popleft()
        state_id = board_to_tuple(state.board)
        if state_id in visited:
            continue
        visited.add(state_id)
        nodes_expanded += 1
        
        if is_goal(state, row_clues, col_clues):
            return state, nodes_expanded
        
        for succ in get_successors(state, n):
            # Only add successor if it is valid so far
            if is_valid_state(succ, row_clues, col_clues):
                frontier.append(succ)
    return None, nodes_expanded

# ---------------------------
# Solve Nonogram with BFS Function
# ---------------------------

def solve_nonogram_bfs(column_clues, row_clues):
    """
    Solve the Nonogram puzzle using BFS.
    
    Parameters:
      column_clues (list of lists): Clues for each column.
      row_clues (list of lists): Clues for each row.
      
    Returns:
      solution_state: The final board state if a solution is found (None if unsolvable).
      game_states_reached (int): Number of game states expanded during search.
    """
    n = len(row_clues)  # assuming square board (n x n)
    initial_board = [[-1 for _ in range(n)] for _ in range(n)]
    initial_state = NonogramState(initial_board, index=0, cost=0, parent=None)
    
    solution, game_states_reached = search_bfs(initial_state, row_clues, column_clues, n)
    return solution, game_states_reached

# ---------------------------
# Example Usage
# ---------------------------

if __name__ == '__main__':
    # Given puzzle clues
    column_clues = [[1,1,1], [2,1], [3], [2], [2,1]]
    row_clues = [[3,1], [2,1], [1,1], [1,1], [1,1]]
    
    solution, states_count = solve_nonogram_bfs(column_clues, row_clues)
    
    if solution:
        print("Solution found!")
        print("Final board configuration:")
        render_board(solution.board)
        print("Number of game states reached:", states_count)
    else:
        print("No solution found.")
        print("Number of game states reached:", states_count)