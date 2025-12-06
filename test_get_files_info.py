import unittest
import os
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_current_directory(self):
        """Test get_files_info for current directory"""
        result = get_files_info("calculator", ".")
        
        # Format output to match expected format
        print(f"\nget_files_info(\"calculator\", \".\"):")
        print("\nResult for current directory:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains expected format
        self.assertIn("file_size=", result)
        self.assertIn("is_dir=", result)
    
    def test_pkg_directory(self):
        """Test get_files_info for pkg subdirectory"""
        result = get_files_info("calculator", "pkg")
        
        # Format output to match expected format
        print(f"\nget_files_info(\"calculator\", \"pkg\"):")
        print("\nResult for 'pkg' directory:")
        print(result)
        
        # Verify it's not an error
        self.assertFalse(result.startswith("Error:"))
        # Verify it contains expected format
        self.assertIn("file_size=", result)
        self.assertIn("is_dir=", result)
    
    def test_outside_directory_absolute_path(self):
        """Test get_files_info with absolute path outside working directory"""
        result = get_files_info("calculator", "/bin")
        
        # Format output to match expected format
        print(f"\nget_files_info(\"calculator\", \"/bin\"):")
        print("\nResult for '/bin' directory:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("Cannot list", result)
        self.assertIn("/bin", result)
        self.assertIn("outside the permitted working directory", result)
    
    def test_outside_directory_relative_path(self):
        """Test get_files_info with relative path outside working directory"""
        result = get_files_info("calculator", "../")
        
        # Format output to match expected format
        print(f"\nget_files_info(\"calculator\", \"../\"):")
        print("\nResult for '../' directory:")
        print(f"    {result}")
        
        # Verify it returns an error
        self.assertTrue(result.startswith("Error:"))
        self.assertIn("Cannot list", result)
        self.assertIn("../", result)
        self.assertIn("outside the permitted working directory", result)


if __name__ == "__main__":
    unittest.main()

