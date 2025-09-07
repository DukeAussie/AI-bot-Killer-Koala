# functions/safe_path.py
import os

PROJECT_ROOT = os.path.abspath(os.getcwd())  # sandbox root (repo root)

def safe_path(path: str, working_directory: str = None) -> str:
    """
    Resolve `path` safely inside the working directory (or PROJECT_ROOT by default).
    Prevents directory traversal (`..`) and absolute paths outside sandbox.
    """

    # Default to project root unless a working dir is passed
    base_dir = os.path.abspath(working_directory or PROJECT_ROOT)

    # Reject absolute paths directly
    if os.path.isabs(path):
        raise ValueError(f"Absolute paths are forbidden: {path}")

    # Normalize against base_dir
    candidate = os.path.abspath(os.path.join(base_dir, path))

    # Ensure it's still inside the base_dir (sandbox)
    if not candidate.startswith(base_dir + os.sep):
        raise ValueError(f"Access to '{path}' is outside the permitted sandbox.")

    return candidate
