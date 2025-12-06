import unittest
import os
from functions.run_python_file import run_python_file


class TestRunPythonFile(unittest.TestCase):
    def test_main_py_no_args(self):
        """Test run_python_file for main.py without arguments"""
        result = run_python_file("calculator", "main.py")
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"main.py\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains the usage instructions
        self.assertIn("Calculator App", result)
        self.assertIn("Usage", result)
    
    def test_main_py_with_args(self):
        """Test run_python_file for main.py with arguments"""
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"main.py\", [\"3 + 5\"]):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains output (the calculator result)
        self.assertGreater(len(result), 0)
    
    def test_tests_py(self):
        """Test run_python_file for tests.py"""
        result = run_python_file("calculator", "tests.py")
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"tests.py\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains test output (should show test results)
        self.assertGreater(len(result), 0)
    
    def test_outside_directory_relative_path(self):
        """Test run_python_file with relative path outside working directory"""
        result = run_python_file("calculator", "../main.py")
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"../main.py\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("Cannot execute", result)
        self.assertIn("../main.py", result)
        self.assertIn("outside the permitted working directory", result)
    
    def test_nonexistent_file(self):
        """Test run_python_file with non-existent file"""
        result = run_python_file("calculator", "nonexistent.py")
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"nonexistent.py\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("File", result)
        self.assertIn("not found", result)
        self.assertIn("nonexistent.py", result)
    
    def test_non_python_file(self):
        """Test run_python_file with non-Python file"""
        result = run_python_file("calculator", "lorem.txt")
        
        # Format output to match expected format
        print(f"\nrun_python_file(\"calculator\", \"lorem.txt\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("is not a Python file", result)
        self.assertIn("lorem.txt", result)


if __name__ == "__main__":
    unittest.main()

