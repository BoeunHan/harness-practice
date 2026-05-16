from workflow import run_workflow
from tools.file_explorer import find_project_folder_from_docs


def get_user_input():
    print("\n========= AI HARNESS INPUT =========")

    project = input("\n🛠️  시작할 프로젝트 이름을 입력하세요: ").strip()

    project_folder = find_project_folder_from_docs(project)

    while not project_folder:
        print(f"❌ docs에서 '{project}' 프로젝트를 찾을 수 없습니다.")
        print("❌ 프로젝트 폴더를 생성하거나 target.json을 생성해주세요.")
        project = input("\n🛠️  시작할 프로젝트 이름을 입력하세요:").strip()
        project_folder = find_project_folder_from_docs(project)

    return {"project": project, "project_folder": project_folder}


def main():
    user_input = get_user_input()

    print("\n========= USER INPUT =========\n")

    print(f"PROJECT: {user_input['project']}")

    print("\n==============================\n")

    print(f"\n🚀 워크플로우를 시작합니다...\n")

    result = run_workflow(project=user_input["project"])

    print("\n========= FINAL RESULT =========\n")
    print(result)


if __name__ == "__main__":
    main()
