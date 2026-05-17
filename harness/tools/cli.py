import itertools
import time
import subprocess

from tools.file_explorer import find_project_dir_from_docs


def spinner(stop_event):
    for dots in itertools.cycle(["⚙️", "⚙️  🔨", "⚙️  🔨 🔥"]):
        if stop_event.is_set():
            break
        print(f"\r\033[KLoading {dots}", end="", flush=True)
        time.sleep(0.6)
    print("\r", end="")


def get_project_select_input():
    print("\n========= AI HARNESS INPUT =========")

    project = input("\n🛠️  시작할 프로젝트 이름을 입력하세요:").strip()
    project_dir = find_project_dir_from_docs(project)

    while not project_dir:
        print(f"❌ docs에서 '{project}' 프로젝트를 찾을 수 없습니다.")
        print("❌ 프로젝트 폴더를 생성하거나 target.json을 생성해주세요.")
        project = input("\n🛠️  시작할 프로젝트 이름을 입력하세요:").strip()
        project_dir = find_project_dir_from_docs(project)

    return {"project": project, "project_dir": project_dir}


def get_user_confirm_input(message: str, enterDefault: bool = True) -> bool:
    """
    사용자에게 단계 진행 여부를 확인하는 함수

    Args:
        message: 출력할 설명 메시지
        enterDefault: 엔터만 눌렀을 때 기본값

    Returns:
        True = 진행, False = 중단
    """

    suffix = " [Y/N] (디폴트는 Y): " if enterDefault else " [Y/N] (디폴트는 N): "

    while True:
        user_input = input(f"\n{message}{suffix}").strip().lower()

        if user_input == "" and enterDefault:
            return True
        if user_input == "" and not enterDefault:
            return False

        if user_input in ["Y", "y", "yes"]:
            return True
        if user_input in ["N", "n", "no"]:
            return False

        print("👉 Y 또는 N으로 입력해주세요.")


def run_command(command: str, cwd=None):
    ALLOWED_COMMANDS = ["npm install", "npm run typecheck", "npm run build"]

    if command not in ALLOWED_COMMANDS:
        raise Exception(f"실행 금지된 명령어입니다. : {command}")

    result = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
    )

    return result.returncode == 0
