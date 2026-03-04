import unittest 
from Calculator import Calculator

class TestOperation(unittest.TestCase):
    
    def test_sum(self):
        calculation = Calculator(2, 2)
        self.assertEqual(calculation.get_sum(), 4, "Answer is not 4")

    def test_diff(self):
        calculation = Calculator(9, 2)
        self.assertEqual(calculation.get_difference(), 6, "Answer is not 6")

if __name__ == "__main__":
    unittest.main()
