import unittest
from solution import solution

class TestSolution(unittest.TestCase):

    def test1(self):
        matrix_A = [[1]]
        matrix_B = [[-1]]
        n = 1
        expected_output = [1, -1]
        self.assertEqual(solution(matrix_A, matrix_B, n), expected_output)

    def test2(self):
        matrix_A = [[1, 2], [3, 4]]
        matrix_B = [[5, 6], [7, 8]]
        n = 1
        expected_output = [1, 2, 4, 3, 5, 6, 8, 7]
        self.assertEqual(solution(matrix_A, matrix_B, n), expected_output)

    def test3(self):
        matrix_A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        matrix_B = [[10, 11, 12], [13, 14, 15], [16, 17, 18]]
        n = 2
        expected_output = [1, 2, 3, 6, 9, 8, 7, 4, 5, 10, 11, 12, 15, 18, 17, 16, 13, 14]
        self.assertEqual(solution(matrix_A, matrix_B, n), expected_output)

    def test4(self):
        matrix_A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        matrix_B = [[11, 12, 13, 14], [15, 16, 17, 18], [19, 20, 21, 22], [23, 24, 25, 26]]
        n = 2
        expected_output = [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10, 11, 12, 13, 14, 18, 22, 26, 25, 24, 23, 19, 15, 16, 17, 21, 20]
        self.assertEqual(solution(matrix_A, matrix_B, n), expected_output)

    def test5(self):
        matrix_A = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
        matrix_B = [[26, 27, 28, 29, 30], [31, 32, 33, 34, 35], [36, 37, 38, 39, 40], [41, 42, 43, 44, 45], [46, 47, 48, 49, 50]]
        n = 3
        expected_output = [1, 2, 3, 4, 5, 10, 15, 20, 25, 24, 23, 22, 21, 16, 11, 6, 7, 8, 9, 14, 19, 18, 17, 12, 13, 26, 27, 28, 29, 30, 35, 40, 45, 50, 49, 48, 47, 46, 41, 36, 31, 32, 33, 34, 39, 44, 43, 42, 37, 38]
        self.assertEqual(solution(matrix_A, matrix_B, n), expected_output)

if __name__ == "__main__":
    unittest.main()