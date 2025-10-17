import os
from config import character_limit
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="get the content of a file in the specified directory along with it character lenght",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read content from, relative to the working directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Check if the path is within the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_full_path):
            return f'Error: "{file_path}" is not a file'

        # Read file content

        with open(abs_full_path, "r") as file:
            content = file.read()

        if len(content) > character_limit:
            content = (
                content[:character_limit]
                + f'[...File "{file_path}" truncated at 10000 characters]'
            )

        return content

    except Exception as e:
        return f"Error: {str(e)}"
