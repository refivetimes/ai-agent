import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, creating it if it doesn't exist or overwriting the existing file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to write to in the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # Ensure the directory exists
        dir_path = os.path.dirname(abs_full_path)
        if dir_path and not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
            except Exception as e:
                return f'Error: Could not create directory for "{file_path}" - {str(e)}'
        
        # Write the file
        try:
            with open(abs_full_path, 'w') as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: could not write to file: "{file_path}" - {str(e)}'
    except Exception as e:
        return f"Error: Failed to check path - {str(e)}"
