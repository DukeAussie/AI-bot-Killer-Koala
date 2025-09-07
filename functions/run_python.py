import os
import subprocess
from google.genai import types
from functions.safe_path import safe_path  # 👈 new helper file

# Opt-in env flag
ALLOW_EXEC = os.getenv("ALLOW_EXEC", "false").lower() == "true"

def run_python_file(file_path: str, args=None, dry_run: bool = False):
    try:
        # Ensure safe path
        abs_file_path = safe_path(file_path)

        # Only allow .py files
        if not abs_file_path.endswith(".py"):
            return f"Error: Only .py files can be executed. Got: {file_path}"

        # Exec disabled by default
        if not ALLOW_EXEC:
            return "Error: Execution is disabled. Set ALLOW_EXEC=true to enable."

        # Build the command
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)

        # Dry-run mode
        if dry_run:
            return f"[DryRun] Would run: {' '.join(commands)}"

        # Run safely
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.getcwd(),  # sandboxed root
        )

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
