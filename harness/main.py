from tools.cli import get_project_select_input
from workflow import run_workflow


def main():
    user_input = get_project_select_input()

    print("\n========= USER INPUT =========\n")

    print(f"PROJECT: {user_input['project']}")

    print("\n==============================\n")

    print(f"\n🚀 워크플로우를 시작합니다...\n")

    run_workflow(project_dir=user_input["project_dir"])

    print(f"\n🖐️  워크플로우가 종료되었습니다. GOOD BYE ~\n")


if __name__ == "__main__":
    main()
