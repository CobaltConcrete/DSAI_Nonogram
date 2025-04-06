from onlinesolver import NonogramSolver

# Define the row and column clues for your nonogram puzzle
ROWS_VALUES = [
    [2], [4], [6], [4, 3], [5, 4], [2, 3, 2], [3, 5], [5], [3], [2], [2], [6]
]
COLS_VALUES = [
    [3], [5], [3, 2, 1], [5, 1, 1], [12], [3, 7], [4, 1, 1, 1], [3, 1, 1], [4], [2]
]

# Optionally, specify a savepath where intermediate results will be saved as images
savepath = './images'  # Replace with the actual path

# Create an instance of the NonogramSolver with the defined clues
solver = NonogramSolver(ROWS_VALUES=ROWS_VALUES, COLS_VALUES=COLS_VALUES, savepath=savepath)

# The solver will automatically attempt to solve the puzzle and display/save intermediate solutions.
