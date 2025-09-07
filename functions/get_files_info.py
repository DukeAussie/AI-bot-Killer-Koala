import os

def get_files_info(working_directory, directory="."):
    """
    List the contents of a directory inside the given working_directory.

    Args:
        working_directory (str): Root directory where operations are allowed.
        directory (str): Relative path inside the working_directory.

    Returns:
        str: Directory contents in formatted string, or error message.
    """
    try:
        # Build the absolute paths
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_path, directory))

        # Guardrail: must stay inside working_directory
        if not target_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Must be a directory
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        # Build file info list
        entries = []
        for name in os.listdir(target_path):
            full_path = os.path.join(target_path, name)
            is_dir = os.path.isdir(full_path)
            try:
                size = os.path.getsize(full_path)
            except Exception as e:
                # If size retrieval fails, fall back gracefully
                size = f"Error getting size: {e}"

            entries.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(entries)

    except Exception as e:
        return f"Error: {e}"
