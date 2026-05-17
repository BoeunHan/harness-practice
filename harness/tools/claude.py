from datetime import datetime
import subprocess
import threading
import re

from tools.cli import spinner


# claude code cli wrapper
def run_claude(prompt: str) -> str:
    stop_event = threading.Event()

    thread = threading.Thread(target=spinner, args=(stop_event,))
    thread.start()

    CLUADE_RULE = """
기본 응답 출력 규칙:
- 응답은 반드시 JSON 형식으로 반환한다.
- JSON 외의 다른 설명은 포함하지 않는다.
- 설명이 필요한 경우 JSON 내 적절한 위치에 포함한다.
- 설명은 한글로 작성한다.
"""

    prompt = CLUADE_RULE + "\n\n" + prompt

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

    write_debug_files(prompt, result.stdout.strip())
    return normalize_claude_response(result.stdout.strip())


def normalize_claude_response(text: str) -> str:
    # ```json 제거
    text = re.sub(r"```json|```", "", text).strip()

    # JSON 부분만 추출
    start = text.find("{")
    end = text.rfind("}") + 1

    return text[start:end]


def write_debug_files(prompt: str, response: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    write_file("harness/debug/claude_prompt.txt", f"[{timestamp}]\n\n {prompt}")
    write_file(
        "harness/debug/claude_raw_response.txt", f"[{timestamp}]\n\n {response.strip()}"
    )


def write_file(filePath: str, text: str):
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(text)
