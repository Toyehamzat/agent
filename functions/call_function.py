from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file


# Dictionary mapping function names to actual functions
FUNCTION_MAP = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    """
    Call one of the available functions based on the function_call_part.
    
    Args:
        function_call_part: A types.FunctionCall with .name and .args properties
        verbose: If True, print detailed information about the function call
    
    Returns:
        types.Content with the function response
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)  # Convert to regular dict
    
    # Print function call information
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    # Check if function exists
    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # Add the working_directory argument
    function_args["working_directory"] = "./calculator"
    
    # Call the function
    function_to_call = FUNCTION_MAP[function_name]
    function_result = function_to_call(**function_args)
    
    # Return the result as types.Content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )