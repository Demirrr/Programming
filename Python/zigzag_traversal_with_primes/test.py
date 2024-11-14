import unittest
from solution import zigzag_traverse_and_primes


class TestZigZagTraverse(unittest.TestCase):

    def test_1(self):
        input_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        output = {2: 2, 3: 3, 5: 5, 7: 7}
        self.assertEqual(zigzag_traverse_and_primes(input_matrix), output)

    def test_2(self):
        input_matrix = [
            [10, 21, 32, 43],
            [54, 65, 17, 82],
            [93, 88, 83, 11],
            [22, 32, 42, 52]
        ]
        output = {4: 43, 6: 17, 11: 83, 12: 11}
        self.assertEqual(zigzag_traverse_and_primes(input_matrix), output)

    def test_3(self):
        input_matrix = [
            [2, 2],
            [2, 2]
        ]
        output = {1: 2, 2: 2, 3: 2, 4: 2}
        self.assertEqual(zigzag_traverse_and_primes(input_matrix), output)

    def test_4(self):
        input_matrix = [
            [1]
        ]
        output = {}
        self.assertEqual(zigzag_traverse_and_primes(input_matrix), output)

    def test_5(self):
        input_matrix = [
            [31, 32, 33, 34, 35],
            [36, 37, 38, 41, 42],
            [47, 48, 53, 54, 55],
            [56, 59, 60, 61, 62],
            [67, 68, 71, 72, 73]
        ]
        output = {1: 31, 7: 41, 9: 37, 11: 47, 13: 53, 17: 61, 19: 59, 21: 67, 23: 71, 25: 73}
        self.assertEqual(zigzag_traverse_and_primes(input_matrix), output)


if __name__ == "__main__":
    unittest.main()