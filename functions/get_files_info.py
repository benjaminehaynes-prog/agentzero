import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))
        if os.path.commonpath([absolute_path, target_dir]) != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir): 
            return f'Error: "{directory}" is not a directory'
        files = os.listdir(target_dir)
        reviewed = []
        for filename in files:
            full_path = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(full_path)
            file_size = os.path.getsize(full_path)
            line = f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            reviewed.append(line)
        result = "\n".join(reviewed)
        return result
    except Exception as e:
        return f'Error: {e}'