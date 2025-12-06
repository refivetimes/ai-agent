import os
import subprocess
import sys
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file if it exists in the working directory and is executable.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path of the .py file in the working directory.",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
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
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if the path is actually a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'

        # Check if python file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

    except Exception as e:
        return f"Error: Failed to check if path is file - {str(e)}"

    try:
        # Build command with args
        cmd = [sys.executable, abs_full_path] + args
        res = subprocess.run(cmd, timeout=30, capture_output=True, text=True, cwd=abs_working_dir)
        
        output_parts = []
        if res.stdout:
            output_parts.append(f'STDOUT: {res.stdout}')
        if res.stderr:
            output_parts.append(f'STDERR: {res.stderr}')
        if res.returncode != 0:
            output_parts.append(f'Process exited with code {res.returncode}')
        
        return '\n'.join(output_parts) if output_parts else 'Process completed successfully with no output'
    except subprocess.TimeoutExpired:
        return "Error: executing Python file: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
