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
response = client.models.generate_content(
  model='gemini-2.5-flash',
  contents=messages,
  config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
  )
)
metadata = response.usage_metadata
if metadata is None:
  raise RuntimeError("No metadata available")
if args.verbose:
  prompt_tokens = metadata.prompt_token_count
  response_tokens = metadata.candidates_token_count
  print(f"User prompt: {args.user_prompt}")
  print(f"Prompt tokens: {prompt_tokens}")
  print(f"Response tokens: {response_tokens}")

# Access function calls from the response
func_calls = []
if response.candidates:
    for candidate in response.candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                # Check if this part is a function call
                if hasattr(part, 'function_call') and part.function_call:
                    func_calls.append(part.function_call)

if func_calls:
    from functions.call_function import call_function
    
    # Use current directory as working directory (could be made configurable)
    working_directory = "./calculator"
    
    # Collect function responses to add to conversation
    function_responses = []
    function_response_data = []
    
    for function_call in func_calls:
        result_content = call_function(function_call, working_directory=working_directory, verbose=args.verbose)
        function_responses.append(result_content)
        
        # Capture the function response from parts[0].function_response.response
        if not result_content.parts or len(result_content.parts) == 0:
            raise RuntimeError(f"Function call result has no parts: {function_call.name}")
        
        part = result_content.parts[0]
        if not hasattr(part, 'function_response') or not part.function_response:
            raise RuntimeError(f"Function call result part has no function_response: {function_call.name}")
        
        if not hasattr(part.function_response, 'response'):
            raise RuntimeError(f"Function call result function_response has no response attribute: {function_call.name}")
        
        function_response = part.function_response.response
        function_response_data.append(function_response)
        
        # Print the result if verbose was set
        if args.verbose:
            print(f"-> {function_response}")
    
    # Add function responses to messages for follow-up conversation
    messages.extend(function_responses)
    
    # Continue conversation with function results
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    # Print final response
    text_parts = []
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
    
    if text_parts:
        print(''.join(text_parts))
    elif hasattr(response, 'text') and response.text:
        print(response.text)
else:
    # Print text response if no function calls
    text_parts = []
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
    
    if text_parts:
        print(''.join(text_parts))
    elif hasattr(response, 'text') and response.text:
        print(response.text)
    else:
        print("No response text available")