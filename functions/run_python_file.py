import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file in the specified working directory with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The working directory where the Python file is located.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file path to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command line arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["working_directory", "file_path"],
    ),
)



def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)

        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Check if the path is within the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_full_path):
            return f'Error: "{file_path}" does not exist'

        if not abs_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        cmd = ["python", abs_full_path] + args
        completed_process = subprocess.run(
            cmd, cwd=abs_working_dir, capture_output=True, text=True, timeout=30
        )

        # Format the output
        output = f"Exit code: {completed_process.returncode}\n"
        output += f"Stdout:\n{completed_process.stdout}\n"
        output += f"Stderr:\n{completed_process.stderr}"
        
        return output

    except subprocess.TimeoutExpired:
        return f'Error: Execution of "{file_path}" timed out after 30 seconds'
    except Exception as e:
        return f"Error: {str(e)}"
