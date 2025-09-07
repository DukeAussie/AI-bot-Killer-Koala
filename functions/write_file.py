import os

def write_file(working_directory, file_path, content):
    """
    Safely write (or overwrite) a file inside the working_directory.

    Args:
        working_directory (str): Root directory where operations are allowed.
        file_path (str): Relative path to the file inside working_directory.
        content (str): Text content to write.

    Returns:
        str: Success message or error string prefixed with "Error:".
    """
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_path, file_path))

        # Guardrail: must stay inside working_directory
        if not target_path.startswith(base_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure the parent directory exists
        parent_dir = os.path.dirname(target_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Write (overwrite) the file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
