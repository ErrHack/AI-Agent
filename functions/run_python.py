import os
import subprocess


def run_python_file(working_directory, file_path):
    try:
        abs_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
        if not abs_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        cp = subprocess.run(
            ["python", abs_path],
            timeout=30,
            capture_output=True,
            cwd=abs_working_dir
        )
        output = []
        if cp.stdout: output.append(f'STDOUT: {cp.stdout}')
        if cp.stderr: output.append(f'STDERR: {cp.stderr}')
        if cp.returncode != 0: output.append(f"Process exited with code {cp.returncode}")
        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"