import os
from dotenv import load_dotenv
from google import genai
from google.genai import  types

# ✅ import from root-level call_function.py
from call_function import call_function, available_functions


def generate_content(client, messages, verbose, dry_run, system_instruction):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_instruction,
        ),
    )

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        mode_tag = "[SAFE MODE]" if dry_run else "[UNSAFE MODE]"
        return f"{mode_tag}\n\n{response.text}"

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(
            function_call_part, verbose=verbose, dry_run=dry_run
        )
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="user", parts=function_responses))


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not set in environment")

    client = genai.Client(api_key=api_key)

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, nargs="*", help="Prompt to send to Killer Koala")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--unsafe", action="store_true", help="Enable unsafe mode (allow writes/exec)")
    args = parser.parse_args()

    prompt = " ".join(args.prompt)
    verbose = args.verbose
    dry_run = not args.unsafe

    if verbose:
        print(f"Running in {'UNSAFE' if not dry_run else 'SAFE'} mode")

    system_instruction = "You are Killer Koala, an assistant that can explore files and run code."

    messages = [types.Content(role="user", parts=[types.Part.from_text(text=prompt)])]

    result = generate_content(client, messages, verbose, dry_run, system_instruction)

    if result:
        print(result)


if __name__ == "__main__":
    main()
