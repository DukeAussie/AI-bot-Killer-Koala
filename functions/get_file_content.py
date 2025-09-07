import os
from config import MAX_FILE_CHARS

def get_file_content(working_directory, file_path):
    """
    Safely read a file inside working_directory and return its contents as a string.
    Errors are returned as strings prefixed with "Error:".
    """

    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_path, file_path))

        # Guardrail: must stay inside working_directory
        if not target_path.startswith(base_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Must be a real file
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read content
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Truncate if too long
        if len(content) > MAX_FILE_CHARS:
            return (
                content[:MAX_FILE_CHARS]
                + f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            )

        return content

    except Exception as e:
        return f"Error: {e}"
