def spiral_traverse_and_vowels(grid):
    if not grid or not grid[0]:
        return []

    # Dimensions of the grid
    n, m = len(grid), len(grid[0])
    # Boundaries for spiral traversal
    top, bottom, left, right = 0, n - 1, 0, m - 1

    # List to store the characters in the spiral order
    spiral_sequence = []

    # Spiral traversal
    while top <= bottom and left <= right:
        # Traverse from left to right on the current top row
        for col in range(left, right + 1):
            spiral_sequence.append(grid[top][col])
        top += 1

        # Traverse from top to bottom on the current right column
        for row in range(top, bottom + 1):
            spiral_sequence.append(grid[row][right])
        right -= 1

        # Check if there's a bottom row to traverse from right to left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                spiral_sequence.append(grid[bottom][col])
            bottom -= 1

        # Check if there's a left column to traverse from bottom to top
        if left <= right:
            for row in range(bottom, top - 1, -1):
                spiral_sequence.append(grid[row][left])
            left += 1

    # Find positions of vowels in the spiral sequence
    vowels = {'a', 'e', 'i', 'o', 'u'}
    vowel_positions = [
        i + 1 for i, char in enumerate(spiral_sequence) if char in vowels
    ]

    return vowel_positions
