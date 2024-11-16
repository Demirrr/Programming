""" matrix_boundary_concatenation """
def solution(matrix_A, matrix_B, n):
    def extract_boundary_layers(matrix, num_layers):
        """Extracts the first `num_layers` boundary layers from a square matrix."""
        layers = []
        size = len(matrix)
        for layer in range(num_layers):
            # Top row (left to right)
            layers.extend(matrix[layer][layer:size - layer])
            # Right column (top to bottom, excluding the first already added)
            layers.extend(matrix[row][size - layer - 1] for row in range(layer + 1, size - layer))
            # Bottom row (right to left, excluding the corners)
            if size - layer - 1 > layer:  # Ensure there's a bottom row
                layers.extend(matrix[size - layer - 1][col] for col in range(size - layer - 2, layer - 1, -1))
            # Left column (bottom to top, excluding the corners)
            if size - layer - 1 > layer:  # Ensure there's a left column
                layers.extend(matrix[row][layer] for row in range(size - layer - 2, layer, -1))
        return layers

    # Extract n layers from both matrices
    layers_A = extract_boundary_layers(matrix_A, n)
    layers_B = extract_boundary_layers(matrix_B, n)

    # Concatenate the layers from A and B
    return layers_A + layers_B

if __name__ == "__main__":
    matrix_A = [[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12],
                [13, 14, 15, 16]]

    matrix_B = [[17, 18, 19, 20],
                [21, 22, 23, 24],
                [25, 26, 27, 28],
                [29, 30, 31, 32]]
    n = 2
    assert solution(matrix_A, matrix_B, n)==[1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10, 17, 18, 19, 20, 24, 28, 32, 31, 30, 29, 25, 21, 22, 23, 27, 26]