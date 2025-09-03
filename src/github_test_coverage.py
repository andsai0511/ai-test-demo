import os
import requests
import json
import re
import ast

SRC_PATH = os.getenv("SRC_PATH", "app.py")
TEST_PATH = os.getenv("TEST_PATH", "tests/test_app_generated.py")
LLM_URL = os.getenv("LLM_URL", "http://localhost:11434/api/generate")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
BOT = os.getenv("BOT", "ollama")

prompt = f"""
Write ONLY valid pytest unit tests for all functions in {SRC_PATH}.
Rules:
- Do NOT rewrite {SRC_PATH}.
- Do NOT include explanations or markdown.
- Output must be pure Python code that starts with "import pytest".
- Function names must exactly match those in {SRC_PATH}.
"""

def generate_tests():
    if BOT.lower() != "ollama":
        raise ValueError("Unsupported BOT type")

    # Call Ollama API
    response = requests.post(
        LLM_URL,
        json={"model": LLM_MODEL, "prompt": prompt},
        stream=True
    )

    raw_output = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            raw_output += data.get("response", "")

    print("----- Raw Ollama Output Start -----")
    print(raw_output)
    print("----- Raw Ollama Output End -----")

    # 🧹 Cleanup
    code = raw_output.replace("```", "").strip()

    # Extract only lines starting from "import pytest"
    match = re.search(r"(import pytest[\s\S]*)", code)
    if match:
        code = match.group(1)

    # ✅ Force correct import style if Ollama outputs "import app"
    code = code.replace("import app", "from app import add, subtract, multiply, divide")

    # ✅ Fix bad pytest.raises usage
    code = re.sub(
        r"assert pytest\.raises\(([^,]+),\s*lambda:\s*([^)]+)\)",
        r"with pytest.raises(\1):\n    \2",
        code
    )

    # ✅ Always prepend sys.path fix at the very beginning
    fix = (
        "import sys, os\n"
        "sys.path.append(os.path.dirname(os.path.dirname(__file__)))\n\n"
    )
    code = fix + code

    # ✅ Syntax validation
    try:
        ast.parse(code)
    except SyntaxError as e:
        print("❌ Generated code has syntax errors. Not saving file.")
        print(e)
        return

    # Ensure test folder exists
    os.makedirs(os.path.dirname(TEST_PATH), exist_ok=True)

    # Save
    with open(TEST_PATH, "w") as f:
        f.write(code.strip())

    print(f"✅ Tests generated in {TEST_PATH}")

if __name__ == "__main__":
    generate_tests()
