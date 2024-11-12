import unittest
from solution import solution

class SolutionTests(unittest.TestCase):
    def test1(self):
        self.assertEqual(solution([[1, -2, 3, -4], [5, -6, 7, 8], [-9, 10, -11, 12]]), [(1, 2), (3, 1), (2, 2), (1, 4), (3, 3)])

    def test2(self):
        self.assertEqual(solution([[0, 0], [0, 0], [0, 0]]), [])

    def test3(self):
        self.assertEqual(solution([[-89]]), [(1, 1)])

    def test4(self):
        self.assertEqual(solution([[1, -1],[-1, 1]]), [(1, 2), (2, 1)])

    def test5(self):
        self.assertEqual(solution([[0, -1, 0], [-1, 2, -1], [0, -1, 0]]), [(1, 2), (2, 1), (2, 3), (3, 2)])

    def test6(self):
        self.assertEqual(solution([[-10, 20, -30, 40, -50],[60, -70, 80, -90, 100]]), [(1, 1), (2, 2), (1, 3), (2, 4), (1, 5)])

if __name__ == '__main__':
    unittest.main()