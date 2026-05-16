import subprocess
import threading
import re

from tools.spinner import spinner


# claude code cli wrapper
def run_claude(prompt: str) -> str:
    stop_event = threading.Event()

    thread = threading.Thread(target=spinner, args=(stop_event,))
    thread.start()

    try:
        result = subprocess.run(
            ["claude", "--model", "claude-haiku-4-5"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=True,
        )
    finally:
        stop_event.set()
        thread.join()

    if result.stderr:
        raise Exception("Claude error: " + result.stderr)

    return normalize_claude_response(result.stdout.strip())


def normalize_claude_response(text: str) -> str:
    # ```json 제거
    text = re.sub(r"```json|```", "", text).strip()

    # JSON 부분만 추출
    start = text.find("{")
    end = text.rfind("}") + 1

    return text[start:end]
