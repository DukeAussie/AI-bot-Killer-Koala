def call_function(function_name, args, verbose=False, dry_run=False):
    # Special case: tests.py should run from project root
    if function_name == "run_python_file" and args.get("file_path") == "tests.py":
        args["working_directory"] = "."
    else:
        args["working_directory"] = "./calculator"

    # Inject dry_run into tools that support it
    if function_name in ("write_file", "run_python_file"):
        args["dry_run"] = dry_run

    # Map function names to implementations
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Execute the actual function safely
    try:
        result = function_map[function_name](**args)
    except Exception as e:
        result = f"Error while executing {function_name}: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
