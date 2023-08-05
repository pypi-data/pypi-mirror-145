from matmath.matrices import Matrix
import unittest


class TestMatrix(unittest.TestCase):
    def test_matrix_1(self):
        # ValueError on empty matrix
        with self.assertRaises(ValueError):
            Matrix()


if __name__ == "__main__":
    unittest.main()
