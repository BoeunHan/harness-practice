import json
from pathlib import Path


def build_app_file_content_list(file_paths: list[Path]) -> list[dict]:
    """
    파일 경로 리스트를 받아 각 앱 파일의 내용을 반환한다.

    Args:
        file_paths: 파일 경로 리스트

    Returns:
        파일 내용 객체 리스트
    """
    base_app_dir = Path("app")

    file_contents = []

    for file_path in file_paths:
        full_file_path = base_app_dir / file_path
        content = read_file_content(full_file_path)
        file_contents.append({"path": str(file_path), "content": content})

    return file_contents


def read_file_content(file_path: Path) -> str:
    """
    파일 내용을 읽어서 반환한다.

    Args:
        file_path: 읽을 파일 경로

    Returns:
        파일 내용 문자열
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ 파일을 읽는 중 오류 발생: {file_path} - {e}")
        return ""


def load_json_file(file_path: str | Path) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        raise Exception(f"❌ 파일을 찾을 수 없습니다: {file_path}")

    except json.JSONDecodeError:
        raise Exception(f"❌ JSON 디코딩 오류: {file_path}")


def write_json_file(file_path: str | Path, data: dict) -> None:
    file_path = Path(file_path)

    # 디렉토리 없으면 생성
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def apply_app_changes(file_path: Path, new_content: str) -> None:
    """
    파일에 새로운 내용을 작성한다.

    Args:
        file_path: 변경할 파일 경로
        new_content: 새로 작성할 내용
    """

    base_app_dir = Path("app")
    full_file_path = base_app_dir / file_path

    full_file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(full_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        raise Exception(f"❌ 파일을 쓰는 중 오류 발생: {full_file_path} - {e}")
