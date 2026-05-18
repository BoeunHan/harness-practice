import questionary
from pathlib import Path


def list_project_dirs():
    docs_dir = Path("docs")
    projects = [p.name for p in docs_dir.iterdir() if p.is_dir()]
    projects.sort()
    return projects


def get_project_select_input():
    print("\n========= AI HARNESS INPUT =========\n")

    projects = list_project_dirs()

    if not projects:
        print("❌ 프로젝트 디렉토리가 없습니다. 'docs' 폴더에 프로젝트를 추가해주세요.")
        return None

    while True:
        project_foldername = questionary.select(
            "프로젝트를 선택하세요:",
            choices=projects,
        ).ask()

        if project_foldername is None:
            raise Exception("선택이 취소되었습니다.")

        try:
            project_dir = validate_project(project_foldername)
            break
        except Exception as e:
            print(f"\n❌ {e}")
            print("다른 프로젝트를 선택해주세요.\n")

    project_name = project_foldername.split("_", 1)[1]

    return {
        "project": project_name,
        "project_dir": project_dir,
    }


def validate_project(project_foldername: str) -> Path:
    project_dir = Path("docs") / project_foldername
    target_file = project_dir / "target.json"

    if not target_file.exists():
        raise Exception(f"target.json 파일이 존재하지 않습니다: {target_file}")

    return project_dir
