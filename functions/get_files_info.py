import os
from google.genai import types
from functions.safe_path import safe_path


def get_files_info(working_directory, directory="."):
    try:
        target_dir = safe_path(directory, working_directory)

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            is_dir = os.path.isdir(filepath)
            size = os.path.getsize(filepath) if not is_dir else 0
            files_info.append(
                f"- {filename}: file_size={size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. Defaults to current working directory.",
            ),
        },
    ),
)
