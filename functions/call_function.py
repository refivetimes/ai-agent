import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


def call_function(function_call, working_directory=".", verbose=False):
    """
    Calls the appropriate function based on the function_call object.
    
    Args:
        function_call: The function call object from the Gemini API response
        working_directory: The working directory to use for all function calls (default: current directory)
        verbose: Whether to print verbose output
    
    Returns:
        A types.Content object with the function response
    """
    if verbose:
        print(f"Calling function: {function_call.name}")
        if hasattr(function_call, 'args') and function_call.args:
            print(f"  Arguments: {function_call.args}")
    
    # Get function name and args
    function_name = function_call.name
    args = {}
    if hasattr(function_call, 'args') and function_call.args:
        # Convert args to dict if it's not already
        if isinstance(function_call.args, dict):
            args = function_call.args
        else:
            # Try to convert from object attributes
            args = dict(function_call.args) if hasattr(function_call.args, '__dict__') else {}
    
    try:
        # Route to the appropriate function
        if function_name == "get_files_info":
            directory = args.get("directory", ".")
            result = get_files_info(working_directory, directory)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )
        
        elif function_name == "get_file_content":
            file_path = args.get("file_path")
            if file_path is None:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": "file_path parameter is required"},
                        )
                    ],
                )
            result = get_file_content(working_directory, file_path)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )
        
        elif function_name == "write_file":
            file_path = args.get("file_path")
            if file_path is None:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": "file_path parameter is required"},
                        )
                    ],
                )
            content = args.get("content", "")
            result = write_file(working_directory, file_path, content)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )
        
        elif function_name == "run_python_file":
            file_path = args.get("file_path")
            if file_path is None:
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": "file_path parameter is required"},
                        )
                    ],
                )
            # Get optional args parameter (should be a list)
            script_args = args.get("args", [])
            if not isinstance(script_args, list):
                script_args = []
            result = run_python_file(working_directory, file_path, script_args)
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )
        
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Exception while calling {function_name}: {str(e)}"},
                )
            ],
        )
