import os


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