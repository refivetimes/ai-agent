import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
    except Exception as e:
        return f"Error: Failed to join paths - {str(e)}"
    
    try:
        # Resolve paths to absolute paths to check if directory is within working_directory
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the resolved path is within the working directory
        # The path must start with the working directory path followed by a separator
        # or be exactly equal to the working directory
        abs_working_dir_normalized = os.path.normpath(abs_working_dir)
        abs_full_path_normalized = os.path.normpath(abs_full_path)
        
        # Check if the full path is within the working directory
        if not (abs_full_path_normalized == abs_working_dir_normalized or 
                abs_full_path_normalized.startswith(abs_working_dir_normalized + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path is actually a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error: Failed to check if path is directory - {str(e)}"

    res = ""
    try:
        directory_contents = os.listdir(abs_full_path)
    except Exception as e:
        return f"Error: Failed to list directory contents - {str(e)}"
    
    for item in directory_contents:
        try:
            item_path = os.path.join(abs_full_path, item)
        except Exception as e:
            return f"Error: Failed to join item path - {str(e)}"
        
        try:
            file_size = os.path.getsize(item_path)
        except Exception as e:
            return f"Error: Failed to get size for '{item}' - {str(e)}"
        
        try:
            is_dir = os.path.isdir(item_path)
        except Exception as e:
            return f"Error: Failed to check if '{item}' is directory - {str(e)}"
        
        new_str = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}\n"
        res += new_str

    return res