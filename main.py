import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Parse command line arguments
verbose = False
prompt = None

for i, arg in enumerate(sys.argv[1:], 1):
    if arg == "--verbose" or arg == "-v":
        verbose = True
    elif prompt is None:
        prompt = arg

if prompt is None:
    print("Error: No prompt provided")
    print("Usage: python main.py [--verbose] <prompt>")
    sys.exit(1)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

"""

model_name = "gemini-2.0-flash-001"


def main():
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # Check if the response contains function calls
    for part in response.candidates[0].content.parts:
        # Check if this part is a function call
        if hasattr(part, "function_call") and part.function_call:
            # Use call_function to handle the function call
            function_call_result = call_function(part.function_call, verbose=verbose)
            
            # Validate the response
            if not hasattr(function_call_result, 'parts') or len(function_call_result.parts) == 0:
                raise RuntimeError("Function call did not return valid types.Content")
            
            if not hasattr(function_call_result.parts[0], 'function_response'):
                raise RuntimeError("Function call result does not contain function_response")
            
            # Print the result if verbose
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # Send the result back to the model for final response
            messages.append(response.candidates[0].content)
            messages.append(function_call_result)

            # Get final response
            final_response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            print(f"\n{final_response.text}")
        elif hasattr(part, "text") and part.text:
            print(f"{part.text}")

    if verbose:
        print(f"\nPrompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
