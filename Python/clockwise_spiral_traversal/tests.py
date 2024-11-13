import unittest
from solution import spiral_traverse_and_vowels

class SpiralTraverseAndVowelsTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(spiral_traverse_and_vowels([['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l']]), [1, 9, 10])

    def test2(self):
        self.assertEqual(spiral_traverse_and_vowels([['o'], ['r'], ['a'], ['l']]), [1, 3])

    def test3(self):
        self.assertEqual(spiral_traverse_and_vowels([['w', 'e', 's'], ['i', 'i', 't'], ['l', 'i', 'f'], ['e', '.', '!']]), [2, 8, 10, 11, 12])

    def test4(self):
        self.assertEqual(spiral_traverse_and_vowels([['w'], ['a'], ['c'], ['h'], ['i'], ['n'], ['g']]), [2, 5])

    def test5(self):
        self.assertEqual(spiral_traverse_and_vowels([['a']]), [1])

if __name__ == '__main__':
    unittest.main()