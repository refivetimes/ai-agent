import os
from functions.config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a file if it exists, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the file in the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
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
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is actually a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Error: Failed to check path - {str(e)}"

    try:
        with open(abs_full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        return file_content_string
    except Exception as e:
        return f'Error: failed to read contents of file: "{file_path}"'
