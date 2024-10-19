# Puzzle for October 2024 

from itertools import permutations

# Function to create the 6x6 grid with A, B, C placed in their correct positions
def create_grid(A, B, C):
    # Initialize an empty grid
    grid = []
    
    # Create each row based on the pattern of A, B, and C in the problem
    for row in range(6):  # 6 rows
        current_row = []
        if row <= 1:
            current_row = [A, A, A, B, B, C]
        elif row <= 3:
            current_row = [A, A, B, B, C, C]
        else:
            current_row = [A, B, B, C, C, C]
        grid.append(current_row)
    
    return grid

# Function to calculte the trip score based on the array placeholders
def calculate_trip_score(trip, grid):
    score = grid[trip[0][0]][trip[0][1]]  # Start score at the first position
    
    for i in range(1, len(trip)):
        current_value = grid[trip[i-1][0]][trip[i-1][1]]
        next_value = grid[trip[i][0]][trip[i][1]]
        if current_value != next_value:
            score *= next_value  # Multiply score if the move is between different integers
        else:
            score += next_value  # Add to the score if the move is between the same integers
    return score

# Check if a knight move is valid within the grid
def is_valid_move(pos):
    return 0 <= pos[0] < 6 and 0 <= pos[1] < 6

# DFS to find all valid knight's paths between start and end positions
def find_knight_paths(start, end, max_depth=10):
    paths = []

    def dfs(current_pos, path, visited):
        if current_pos == end:
            paths.append(path[:])  # Save the path when the end position is reached
            return
        if len(path) > max_depth:
            return  # Stop if we exceed the max allowed moves
        for move in knight_moves:
            next_pos = (current_pos[0] + move[0], current_pos[1] + move[1])
            if is_valid_move(next_pos) and next_pos not in visited:
                visited.add(next_pos)
                path.append(next_pos)
                dfs(next_pos, path, visited)
                # Backtrack
                visited.remove(next_pos)
                path.pop()

    dfs(start, [start], set([start]))  # Start DFS from the start position
    return paths

# Convert board notation to grid indices
def board_to_index(pos):
    col = ord(pos[0]) - ord('a')  # Convert letter (column) to index ('a' -> 0, 'b' -> 1, etc.)
    row = int(pos[1]) - 1  # Convert row to 0-based index (row 1 -> 0, row 6 -> 5)
    return (row, col)

# Convert grid index to board notation
def path_index_to_board(path):
    tbl = ['a', 'b', 'c', 'd', 'e', 'f']
    paths = []
    for row, col in path:
        col = tbl[col]  # Convert index to letters
        row = str(row + 1)  # Convert row 
        paths.append(col+row+',')
    paths[-1] = paths[-1][0:-1] # Take out the last comma
    return paths



# Define the two starting and finishing points
start1 = board_to_index('a1')
end1 = board_to_index('f6')
start2 = board_to_index('a6')
end2 = board_to_index('f1')

# All possible knight moves
knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

# Find paths for each trip
paths_a1_f6 = find_knight_paths(start1, end1)
paths_a6_f1 = find_knight_paths(start2, end2)

# Try all distinct permutations of A, B, C and minimize the sum A + B + C
best_solution = None
min_sum = float('inf')

for A, B, C in permutations(range(1, 20), 3):  # Try values of A, B, C
    grid = create_grid(A, B, C)  # Create the grid
    
    for path1 in paths_a1_f6:
        score1 = calculate_trip_score(path1, grid)  # Calculate score for path from a1 to f6
        if score1 == 2024:
            for path2 in paths_a6_f1:
                score2 = calculate_trip_score(path2, grid)  # Calculate score for path from a6 to f1
                if score2 == 2024:
                    total_sum = A + B + C
                    if total_sum < min_sum:  # Check if this is the smallest sum so far
                        min_sum = total_sum
                        best_solution = (A, B, C, path1, path2)

# Print the best solution found
if best_solution:
    A, B, C, path1, path2 = best_solution
    print(f"Best A, B, C: {A}, {B}, {C}")
    print(f"Path a1 to f6: {path1}")
    print(f"Path a6 to f1: {path2}")
    print(f"Minimal sum A + B + C: {min_sum}")
    path1_board = path_index_to_board(path1)
    path2_board = path_index_to_board(path2)
    print("Solution: ", A, ",", B, ",", C, ",", *path1_board, ",", *path2_board, sep='')
else:
    print("No solution found")
