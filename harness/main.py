
from workflow import run_workflow


def get_user_input():
    print("\n========= AI HARNESS INPUT =========")

    prompt = input("🎯 프롬프트를 입력하세요 (간단한 목표 등): ").strip()


    project = input("\n🛠️  docs에서 참조할 프로젝트 이름을 입력하세요 (선택, 건너뛰려면 엔터): ").strip()
    if project == "":
        project = None


    files = []
    print("\n📁 작업에 참고할 파일 경로를 하나씩 입력하세요. ('q'을 입력하여 파일 추가 종료)")
  
    while True:
        file_path = input("파일> ").strip()

        if file_path.lower() == "q":
            break

        if file_path == "":
            continue

        files.append(file_path)

    return {
        "prompt": prompt,
        "project": project,
        "files": files,
    }


def main():
    user_input = get_user_input()

    print("\n========= USER INPUT =========\n")

    for key, value in user_input.items():
        print(f"{key.capitalize()}: {value}")

    print("\n==============================\n")

    print(f"\n🚀 워크플로우를 시작합니다...\n")

    result = run_workflow(
        prompt=user_input["prompt"],
        project=user_input["project"],
        files=user_input["files"],
    )

    print("\n========= FINAL RESULT =========\n")
    print(result)


if __name__ == "__main__":
    main()