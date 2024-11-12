def solution(matrix):
    n = len(matrix)  # Number of rows
    m = len(matrix[0])  # Number of columns
    result = []

    i, j = 0, 0
    down_left = False  # Start by moving up-right after the initial right step

    while i < n and j < m:
        # Check if the current cell contains a negative value
        if matrix[i][j] < 0:
            result.append((i + 1, j + 1))  # Append the 1-based index of negative values

        # Zigzag traversal logic
        if down_left:
            # Move down-left
            if i + 1 < n and j - 1 >= 0:
                i += 1
                j -= 1
            else:
                # Switch to up-right movement at the boundary
                down_left = False
                if i + 1 < n:
                    i += 1
                else:
                    j += 1
        else:
            # Move up-right
            if i - 1 >= 0 and j + 1 < m:
                i -= 1
                j += 1
            else:
                # Switch to down-left movement at the boundary
                down_left = True
                if j + 1 < m:
                    j += 1
                else:
                    i += 1

    return result
