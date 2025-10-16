import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        
        # Get absolute paths for security validation
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        
        # Check if the path is within the working directory
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the path exists and is a directory
        if not os.path.exists(abs_full_path):
            return f'Error: "{directory}" does not exist'
        
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
        
        # List directory contents
        items = []
        for item in os.listdir(abs_full_path):
            item_path = os.path.join(abs_full_path, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            items.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        
        return "\n".join(items)
    
    except Exception as e:
        return f"Error: {str(e)}"
