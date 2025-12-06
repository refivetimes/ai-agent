import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
  raise RuntimeError ("api key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.prompt`
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)

# Use current directory as working directory (could be made configurable)
working_directory = "./calculator"

# Set working directory in call_function module
import functions.call_function as call_function_module
call_function_module.working_directory = working_directory

# Maximum iterations for the conversation loop
max_iterations = 20

def generate_content(client, messages, verbose):
    from functions.call_function import call_function
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    # 1) Add model response to messages
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content is not None:
                function_call_content = candidate.content
                messages.append(function_call_content)
    
    # 2) If no function calls, we're done
    if not response.function_calls:
        # no tools to run
        return response.text
    
    # 3) Execute function calls
    else:
        function_responses = []
        for function_call in response.function_calls:
            # Always print function calls
            print(f" - Calling function: {function_call.name}")
            function_call_result = call_function(function_call, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
        
        if not function_responses:
            raise Exception("no function responses generated, exiting.")
        
        # 4) Add function results as a new user message
        messages.append(types.Content(role="user", parts=function_responses))
        
        # Return None to signal continuation
        return None

# Main conversation loop
for iteration in range(max_iterations):
    try:
        result = generate_content(client, messages, args.verbose)
        
        # If result is not None, we're done - print and break
        if result is not None:
            print("Final response:")
            print(result)
            break
        
        # If result is None, continue the loop
        continue
    
    except Exception as e:
        print(f"Error in iteration {iteration + 1}: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        break

# Check if we hit max iterations
if iteration == max_iterations - 1:
    print(f"\nReached maximum iterations ({max_iterations}). Stopping.")
