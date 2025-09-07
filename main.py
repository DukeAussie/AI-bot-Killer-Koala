import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.call_function import call_function, available_functions
from config import system_prompt


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--unsafe",
        action="store_true",
        help="Allow write/exec (⚠ dangerous, use only locally)",
    )
    args = parser.parse_args()

    dry_run = not args.unsafe  # ✅ safe mode default

    if args.unsafe:
        print(
            "\n⚠️  UNSAFE MODE ENABLED ⚠️\n"
            "Writes and subprocess execution are now allowed!\n"
            "Only use this mode locally — DO NOT run in production.\n"
        )

    # Inject SAFE/UNSAFE mode into system prompt
    mode_message = (
        "Current mode: SAFE — only read operations are allowed."
        if dry_run
        else "Current mode: UNSAFE — write and execution tools are available."
    )
    system_instruction = f"{system_prompt}\n\n{mode_message}"

    client = genai.Client(api_key=None)  # assumes GEMINI_API_KEY in .env
    messages = []  # conversation history

    try:
        while True:
            final_response = generate_content(
                client, messages, args.verbose, dry_run, system_instruction
            )
            print(final_response)
            break
    except Exception as e:
        print(f"Error in generate_content: {e}")


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


if __name__ == "__main__":
    main()
