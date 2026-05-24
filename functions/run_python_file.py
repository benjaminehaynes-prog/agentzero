import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        absolute_working_path = os.path.normpath(os.path.join(absolute_path, file_path))
        if os.path.commonpath([absolute_path, absolute_working_path]) != absolute_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_working_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not absolute_working_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", absolute_working_path]
        if args is not None:
            command.extend(args)
        completedprocess = subprocess.run(command, cwd=absolute_path, capture_output=True, text=True, timeout = 30)
        outputstring = []
        if completedprocess.returncode != 0:
            outputstring.append(f"Process exited with code {completedprocess.returncode}")
        if len(completedprocess.stdout) == 0 and len(completedprocess.stderr) == 0:
            outputstring.append("No output produced")
        else:
            outputstring.append(f"STDOUT: {completedprocess.stdout}")
            outputstring.append(f"STDERR: {completedprocess.stderr}")
        return "\n".join(outputstring)
    except Exception as e:
        return f"Error: executing Python file: {e}"
