def find_peak(grid, start_row, start_col) -> int:
    rows, cols = len(grid), len(grid[0])
    altitude = grid[start_row][start_col]
    # Check North, East, South, West for higher altitude
    for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        r, c = start_row + dr, start_col + dc
        if 0 <= r < rows and 0 <= c < cols and grid[r][c] > altitude:
            altitude = grid[r][c]
    return altitude
def find_next_peak_coordinates(matrix, row, col):
    rows, cols = len(matrix), len(matrix[0])
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    current_height = matrix[row][col]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if (0 <= r < rows and 0 <= c < cols) and matrix[r][c] > current_height:  # Fill in the condition
            return r, c
    return row, col
def path_traverse(elevation_map, start_x, start_y):
    # Get the current elevation at the starting position
    current_height = elevation_map[start_x][start_y]

    # Define possible moves (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Track the best next position
    best_position = None
    highest_elevation = current_height

    # Check each adjacent position
    for dx, dy in directions:
        new_x, new_y = start_x + dx, start_y + dy

        # Ensure new position is within bounds
        if 0 <= new_x < len(elevation_map) and 0 <= new_y < len(elevation_map[0]):
            adjacent_height = elevation_map[new_x][new_y]

            # Check if the adjacent position has a higher elevation
            if adjacent_height > highest_elevation:
                highest_elevation = adjacent_height
                best_position = (new_x, new_y)

    # Return the best position if found; otherwise, None
    return best_position

# Example mountain terrain grid
mountain = [[1, 2, 3],
            [2, 5, 7],
            [4, 6, 9]]
print(f"the altitude of the highest peak reachable {find_peak(mountain, 0, 1)}")
# Hiking exploration example where the hiker looks for a higher peak around
print("Next peak at coordinates:", find_next_peak_coordinates(mountain, 0, 1))

if next_step := path_traverse(mountain, 0,1):
    print("Next step to higher elevation:", next_step)
else:
    print("No higher adjacent step found.")
