import unittest
import os
from functions.get_file_content import get_file_content
from functions.config import MAX_CHARS


class TestGetFileContent(unittest.TestCase):
    def test_lorem_txt(self):
        """Test get_file_content for lorem.txt and verify truncation"""
        result = get_file_content("calculator", "lorem.txt")
        
        # Format output to match expected format
        print(f"\nget_file_content(\"calculator\", \"lorem.txt\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it's truncated to MAX_CHARS
        self.assertLessEqual(len(result), MAX_CHARS)
        # Verify it contains some content
        self.assertGreater(len(result), 0)
    
    def test_main_py(self):
        """Test get_file_content for main.py"""
        result = get_file_content("calculator", "main.py")
        
        # Format output to match expected format
        print(f"\nget_file_content(\"calculator\", \"main.py\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains some content
        self.assertGreater(len(result), 0)
    
    def test_pkg_calculator_py(self):
        """Test get_file_content for pkg/calculator.py"""
        result = get_file_content("calculator", "pkg/calculator.py")
        
        # Format output to match expected format
        print(f"\nget_file_content(\"calculator\", \"pkg/calculator.py\"):")
        print("\nResult:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains some content
        self.assertGreater(len(result), 0)
    
    def test_outside_directory_absolute_path(self):
        """Test get_file_content with absolute path outside working directory"""
        result = get_file_content("calculator", "/bin/cat")
        
        # Format output to match expected format
        print(f"\nget_file_content(\"calculator\", \"/bin/cat\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("Cannot read", result)
        self.assertIn("/bin/cat", result)
        self.assertIn("outside the permitted working directory", result)
    
    def test_nonexistent_file(self):
        """Test get_file_content with non-existent file"""
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        
        # Format output to match expected format
        print(f"\nget_file_content(\"calculator\", \"pkg/does_not_exist.py\"):")
        print("\nResult:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("File not found", result)
        self.assertIn("does_not_exist.py", result)


if __name__ == "__main__":
    unittest.main()

