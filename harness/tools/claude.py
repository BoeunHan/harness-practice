import subprocess
import threading
from datetime import datetime
from tools.cli import spinner

CLUADE_RULE = """
공통 규칙:
- 설명은 한글로 작성한다.
- 작업 완료 후 즉시 종료해라.
- 추가로 필요한 파일은 직접 읽어서 확인한다.

프로젝트 규칙:
- 프로젝트 루트는 app/ 디렉토리이다.

"""

CLAUDE_PATH = r"C:\Users\hboeu\AppData\Roaming\npm\claude.cmd"
CLAUDE_HAIKU = "claude-haiku-4-5"
CLAUDE_SONNET = "claude-sonnet-4-6"


# claude code cli wrapper
def run_claude(prompt: str):

    stop_event = threading.Event()

    thread = threading.Thread(target=spinner, args=(stop_event,))
    thread.start()

    full_prompt = CLUADE_RULE + "\n\n" + prompt

    write_debug_file("harness/debug/claude_prompt.txt", prompt)
    try:
        subprocess.run(
            [
                CLAUDE_PATH,
                "--model",
                CLAUDE_SONNET,
                "--permission-mode",
                "acceptEdits",
                "-p",
            ],
            input=full_prompt,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as e:
        print("❌ Claude 실행 중 오류 발생: ", e)
    finally:
        stop_event.set()
        thread.join()


def write_debug_file(filePath: str, text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n\n {text}")
