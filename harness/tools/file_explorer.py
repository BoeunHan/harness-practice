from pathlib import Path


def find_project_folder_from_docs(project_name: str) -> Path | None:
    """
    docs 디렉토리 내부에서 프로젝트 폴더를 찾는다.

    Args:
        project_name: 찾을 프로젝트 폴더 이름

    Returns:
        Path 객체 또는 None
    """

    base_path = Path("docs")

    if not base_path.exists():
        return None

    for path in base_path.iterdir():
        if path.is_dir():
            folder_name = path.name

            # 폴더에 숫자 제거
            normalized_name = (
                folder_name.split("_", 1)[1] if "_" in folder_name else folder_name
            )

            # target.json 존재 여부 확인
            target_file = path / "target.json"

            if normalized_name == project_name and target_file.exists():
                return path

    return None
