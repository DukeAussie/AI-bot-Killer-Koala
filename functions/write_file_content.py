import os
from google.genai import types
from functions.safe_path import safe_path  # 👈 create this helper file once

# Writes disabled by default
ALLOW_WRITES = os.getenv("ALLOW_WRITES", "false").lower() == "true"

def write_file(working_directory, file_path, content, dry_run: bool = False):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = safe_path(file_path, abs_working_dir)  # 👈 enforce sandbox

        # Writes disabled unless explicitly enabled
        if not ALLOW_WRITES:
            return (
                f"Error: Writing is disabled by default. "
                f"Set ALLOW_WRITES=true in your environment to enable."
            )

        # Dry-run mode
        if dry_run:
            return (
                f"[DryRun] Would write {len(content)} characters to: {abs_file_path}\n"
                f"---\n{content}\n---"
            )

        # Ensure parent directories exist
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)

        if os.path.exists(abs_file_path) and os.path.isdir(abs_file_path):
            return f'Error: "{file_path}" is a directory, not a file'

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)
