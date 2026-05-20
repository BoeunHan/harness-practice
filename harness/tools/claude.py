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
                "cmd.exe",
                "/c",
                "claude",
                "--model",
                CLAUDE_SONNET,
                "--permission-mode",
                "acceptEdits",
                "-p",
            ],
            input=full_prompt,
            check=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stderr=subprocess.PIPE,  # 에러 내용 수집
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            f"\n❌ Claude 실행 실패 (Exit Code {e.returncode})\n{e.stderr}"
        ) from None
    except FileNotFoundError:
        raise Exception("\n❌ 지정된 경로에서 Claude CLI를 찾을 수 없습니다:") from None
    except Exception as e:
        raise Exception(f"\n❌ 예상치 못한 오류 발생: {e}") from None
    finally:
        stop_event.set()
        thread.join()


def write_debug_file(filePath: str, text: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\n\n {text}")
