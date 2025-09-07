from dotenv import load_dotenv
import os
import sys
from google import genai
#hardcoded string variable that is simple
system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    # 1) Parse verbose and remove the flag
    verbose = False
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")

    # 2) Validate there’s a remaining prompt
    if len(sys.argv) < 2:
        print("Error: no prompt provided")
        sys.exit(1)

    # 3) Build prompt once
    prompt = " ".join(sys.argv[1:])

    # 4) If verbose: print the user prompt
    if verbose:
        print(f"User prompt: {prompt}")

    # 5) Call the model once
    from google.genai import types

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    # 6) Print response text
    print(response.text)

    # 7) If verbose: print token lines
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()
