import os


def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_path, 'r') as f:
            contents = f.read()
        if len(contents) > 10000:
            return contents[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
        return contents
    except Exception as e:
        return f"Error: {e}"