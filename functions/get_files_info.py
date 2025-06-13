import os


def get_files_info(working_directory: str, directory: str = None):
    dir_str = "" if directory == None or directory == '.' else directory
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, dir_str))
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_path):
            return f'Error: "{abs_path}" is not a directory'
        return "\n".join(map(lambda file: f"- {file}: file_size={os.path.getsize(os.path.join(abs_path, file))} bytes, is_dir={os.path.isdir(os.path.join(abs_path, file))}", os.listdir(abs_path)))
    except Exception as e:
        return f"Error: {e}"