import unittest
import os
from functions.write_file import write_file


class TestWriteFile(unittest.TestCase):
    def test_write_lorem_txt(self):
        """Test write_file for lorem.txt"""
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        
        # Format output to match expected format
        print(f"\nwrite_file(\"calculator\", \"lorem.txt\", \"wait, this isn't lorem ipsum\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertIsNotNone(result, "Function should return a result")
        self.assertFalse(result.startswith("Error:"))
        self.assertIn("Successfully wrote", result)
    
    def test_write_pkg_morelorem_txt(self):
        """Test write_file for pkg/morelorem.txt"""
        result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        
        # Format output to match expected format
        print(f"\nwrite_file(\"calculator\", \"pkg/morelorem.txt\", \"lorem ipsum dolor sit amet\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertIsNotNone(result, "Function should return a result")
        self.assertFalse(result.startswith("Error:"))
        self.assertIn("Successfully wrote", result)
    
    def test_outside_directory_absolute_path(self):
        """Test write_file with absolute path outside working directory"""
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        
        # Format output to match expected format
        print(f"\nwrite_file(\"calculator\", \"/tmp/temp.txt\", \"this should not be allowed\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertIsNotNone(result, "Function should return an error message")
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("Cannot write", result)
        self.assertIn("/tmp/temp.txt", result)
        self.assertIn("outside the permitted working directory", result)


if __name__ == "__main__":
    unittest.main()

