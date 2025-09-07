KILLER KOALA AI ASSISTANT
=========================

Killer Koala is an AI-powered coding assistant built on top of Google’s Gemini API.
It can explore your codebase, read files, and (optionally) modify or run them.

By default, Killer Koala runs in SAFE MODE to prevent accidental file changes or code execution.


SETUP
-----

1. Clone the repo:
   git clone <your-repo-url>
   cd <your-repo>

2. Install dependencies:
   pip install -r requirements.txt

3. Add your Gemini API key:
   Create a .env file in the project root with the following line:
   GEMINI_API_KEY=your_api_key_here


SECURITY MEASURES
-----------------

- SAFE MODE (default)
  * Only allows listing files and reading file contents.
  * Blocks file writes and Python execution.
  * All outputs are tagged with [SAFE MODE].

- UNSAFE MODE (optional, opt-in)
  * Enables write_file and run_python_file.
  * Dangerous operations include a ⚠️ warning in console and chat.
  * All outputs are tagged with [UNSAFE MODE].
  * Only use this locally — DO NOT run in production.

- Function-level enforcement
  * get_files_info and get_file_content → always allowed.
  * write_file and run_python_file → blocked unless --unsafe flag is passed.
  * Safe mode cannot be bypassed by the model.


USAGE
-----

Run in Safe Mode (default, recommended):
   python main.py

Run in Unsafe Mode (dangerous):
   python main.py --unsafe

Verbose mode (for debugging):
   python main.py --verbose

Verbose + Unsafe:
   python main.py --verbose --unsafe


AVAILABLE TOOLS
---------------

- get_files_info → List files in a directory.
- get_file_content → Read contents of a file.
- write_file → Write/overwrite a file (UNSAFE ONLY).
- run_python_file → Execute a Python file with optional args (UNSAFE ONLY).


EXAMPLE WORKFLOW
----------------

Example: Exploring the repo and running tests.

1. Start in safe mode:
   python main.py

2. Ask Killer Koala:
   "What files are in the calculator directory?"
   - It will call get_files_info and list files.

3. Ask:
   "Open calculator/config.py"
   - It will call get_file_content and return the code.

4. Modify code (unsafe required):
   python main.py --unsafe
   "Update calculator/config.py to set DEBUG = False"
   - It will call write_file with a ⚠️ warning.

5. Run tests (unsafe required):
   python main.py --unsafe
   "Run tests.py"
   - It will call run_python_file with a ⚠️ warning and show results.


PROTECTED FILES & DIRECTORIES
-----------------------------

Even in `--unsafe` mode, the following are **blocked** for safety:

- `main.py`
- `config.py`
- `prompts.py`
- `call_function.py`

Protected directories:
- `functions/`
- `tests/`

This prevents the AI from rewriting or executing its own core logic.
You can adjust the protection list in `config.py`.


SECURITY MODEL
--------------

- SAFE MODE (default):
  - No writes
  - No execution
  - Exploration only

- UNSAFE MODE (`--unsafe`):
  - Writes and execution allowed
  - ⚠️ Warnings shown before dangerous actions
  - Still respects protected files/directories above


-------------------------------------------------
SAFE MODE is the default. UNSAFE MODE is opt-in.
Always review warnings before allowing writes or execution.
