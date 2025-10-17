import os
from google.genai import types



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the specified path within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write, relative to the working directory.",
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

        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Check if the path is within the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(abs_full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the content to the file
        with open(abs_full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return f'File "{file_path}" written successfully'

    except Exception as e:
        return f"Error: {str(e)}"