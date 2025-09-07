import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    """
    Safely execute a Python file within the working_directory.
    Returns stdout/stderr or an error string.
    """
    try:
        base_path = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(base_path, file_path))

        # Guardrail: must stay inside working_directory
        if not target_path.startswith(base_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # File must exist
        if not os.path.isfile(target_path):
            return f'Error: File "{file_path}" not found.'

        # Must be a .py file
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Run the file with subprocess
        completed_process = subprocess.run(
            ["python3", target_path, *args],
            cwd=base_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout = completed_process.stdout.strip()
        stderr = completed_process.stderr.strip()

        output_parts = []
        if stdout:
            output_parts.append("STDOUT:\n" + stdout)
        if stderr:
            output_parts.append("STDERR:\n" + stderr)
        if completed_process.returncode != 0:
            output_parts.append(f"Process exited with code {completed_process.returncode}")

        if not output_parts:
            return "No output produced."

        return "\n".join(output_parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"
