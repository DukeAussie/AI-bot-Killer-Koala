from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from config import WORKING_DIR

# Tool schemas with safety notes
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files and directories in the working directory (safe).",
    parameters={
        "type": "object",
        "properties": {
            "directory": {"type": "string", "description": "Relative directory path"},
        },
    },
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents from the working directory (safe).",
    parameters={
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Relative path to file"},
        },
        "required": ["file_path"],
    },
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "⚠️ Write or overwrite a file. "
        "This is only allowed when UNSAFE MODE is enabled. "
        "In safe mode, this will be blocked."
    ),
    parameters={
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Relative path to file"},
            "content": {"type": "string", "description": "New file contents"},
        },
        "required": ["file_path", "content"],
    },
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "⚠️ Execute a Python file with optional arguments. "
        "This is only allowed when UNSAFE MODE is enabled. "
        "In safe mode, this will be blocked."
    ),
    parameters={
        "type": "object",
        "properties": {
            "file_path": {"type": "string", "description": "Relative path to Python file"},
            "arguments": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional command-line arguments",
            },
        },
        "required": ["file_path"],
    },
)

# Bundle available functions
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False, dry_run=True):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
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

        elif function_name == "write_file":
            if dry_run:
                result = "❌ Write blocked (safe mode enabled)."
            else:
                warning = "⚠️ Unsafe action: writing to a file."
                file_result = write_file(**args)
                result = f"{warning}\n{file_result}"

        elif function_name == "run_python_file":
            if dry_run:
                result = "❌ Execution blocked (safe mode enabled)."
            else:
                warning = "⚠️ Unsafe action: executing Python code."
                exec_result = run_python_file(**args)
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
                respo
