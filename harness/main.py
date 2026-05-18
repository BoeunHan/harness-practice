from tools.project_selector import get_project_select_input
from workflow import run_workflow


def main():
    user_input = get_project_select_input()

    if not user_input:
        print("❌ 워크플로우가 취소되었습니다.")
        return

    print("\n=========== PROJECT ===========\n")

    print(user_input["project"])

    print("\n===============================\n")

    print(f"\n🚀 워크플로우를 시작합니다...\n")

    run_workflow(project_dir=user_input["project_dir"])

    print(f"\n🖐️  워크플로우가 종료되었습니다. GOOD BYE ~\n")


if __name__ == "__main__":
    main()
