# call_function.py
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file as run_python  # ✅ alias fixed
from functions.write_file_content import write_file
from config import WORKING_DIR


def call_function(function_call_part, verbose=False, dry_run=True):
    """Dispatch function calls safely with optional dry_run mode."""
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR

    result = None

    try:
        if function_name == "get_files_info":
            result = get_files_info(**args)

        elif function_name == "get_file_content":
            result = get_file_content(**args)

        elif function_name == "write_file_content":
            target = args.get("file_path") or args.get("filename")
            if is_blocked_path(target, args.get("working_directory")):
                result = f"❌ Access denied: {target} is protected."
            elif dry_run:
                result = "❌ Write blocked (safe mode enabled)."
            else:
                warning = "⚠️ Unsafe action: writing to a file."
                file_result = write_file_content(**args)
                result = f"{warning}\n{file_result}"

        elif function_name == "run_python":
            target = args.get("file_path") or args.get("filename")
            if is_blocked_path(target, args.get("working_directory")):
                result = f"❌ Access denied: {target} is protected."
            elif dry_run:
                result = "❌ Execution blocked (safe mode enabled)."
            else:
                warning = "⚠️ Unsafe action: executing Python code."
                exec_result = run_python(**args)
                result = f"{warning}\n{exec_result}"

        else:
            result = {"error": f"Unknown function: {function_name}"}

    except Exception as e:
        result = {"error": f"Exception in {function_name}: {e}"}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


# Available tool declarations for Gemini
available_functions = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="get_files_info",
            description="List files in a directory",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "directory": types.Schema(
                        type=types.Type.STRING,
                        description="The directory to list files from, relative to the working directory.",
                    )
                },
                required=["directory"],
            ),
        ),
        types.FunctionDeclaration(
            name="get_file_content",
            description="Read contents of a file",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the file to read, relative to the working directory.",
                    )
                },
                required=["file_path"],
            ),
        ),
        types.FunctionDeclaration(
            name="write_file_content",
            description="Write/overwrite a file (UNSAFE)",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the file to write.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="Content to write to the file.",
                    ),
                },
                required=["file_path", "content"],
            ),
        ),
        types.FunctionDeclaration(
            name="run_python",
            description="Execute a Python file with optional args (UNSAFE)",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="Path to the Python file to execute.",
                    ),
                    "args": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                        description="Optional arguments to pass to the Python file.",
                    ),
                },
                required=["file_path"],
            ),
        ),
    ]
)
