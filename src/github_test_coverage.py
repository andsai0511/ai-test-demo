import os, requests, json

SRC_PATH = os.getenv("SRC_PATH", "app.py")
TEST_PATH = os.getenv("TEST_PATH", "tests/test_app_generated.py")
LLM_URL = os.getenv("LLM_URL", "http://localhost:11434/api/generate")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
BOT = os.getenv("BOT", "ollama")

prompt = f"""
Write pytest unit tests for all functions in {SRC_PATH}.
Include edge cases and clear assertions.
"""

def generate_tests():
    if BOT.lower() == "ollama":
        response = requests.post(
            LLM_URL,
            json={"model": LLM_MODEL, "prompt": prompt},
            stream=True
        )
        code = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                code += data.get("response", "")
    else:
        raise ValueError("Unsupported BOT type")

    os.makedirs(os.path.dirname(TEST_PATH), exist_ok=True)
    with open(TEST_PATH, "w") as f:
        f.write(code)

    print(f"✅ Tests generated in {TEST_PATH}")

if __name__ == "__main__":
    generate_tests()
