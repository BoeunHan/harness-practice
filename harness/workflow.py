import traceback
from pathlib import Path

from agents.planner import planner_agent
from agents.task_decomposer import task_decomposer_agent
from agents.executor import executor_agent
from agents.reviewer import reviewer_agent
from tools.cli import get_user_confirm_input
from tools.file_explorer import (
    apply_app_changes,
    build_app_file_content_list,
    load_json_file,
    write_json_file,
)


def run_workflow(project_dir: Path):

    try:
        print("1️⃣  Planning...")
        target = load_json_file(project_dir / "target.json")
        related_file_contents = build_app_file_content_list(
            target.get("file_paths", [])
        )

        plan = planner_agent(target, related_file_contents)
        write_json_file(project_dir / "01_plan.json", plan)

        print("프로젝트 설계 문서가 생성되었습니다. : " + "01_plan.json")
        if not get_user_confirm_input("Task decomposition을 진행할까요?"):
            print("🟥 워크플로우가 중단되었습니다.")
            return

        print("2️⃣  Decomposing tasks...")

        tasks = task_decomposer_agent(plan)
        write_json_file(project_dir / "02_tasks.json", tasks)

        print("Task 분해가 완료되었습니다. : " + "02_tasks.json")

        tasks = load_json_file(project_dir / "02_tasks.json")
        for task in tasks["tasks"][1:]:
            print("task id: ", task["id"])
            if not get_user_confirm_input(f"{task['id']} Execution을 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            print(f"3️⃣  Executing task: {task['id']}")
            related_file_contents = build_app_file_content_list(
                task.get("related_file_paths", [])
            )

            execution_result = executor_agent(task, related_file_contents)
            execution_result_path = project_dir / f"03_execution_{task['id']}.json"
            write_json_file(execution_result_path, execution_result)

            changed_file_paths = []

            for modified in execution_result.get("modified_files", []):
                print(f"변경된 파일: {modified['path']}")
                apply_app_changes(modified["path"], modified["content"])
                changed_file_paths.append(modified["path"])

            for created in execution_result.get("created_files", []):
                print(f"생성된 파일: {created['path']}")
                apply_app_changes(created["path"], created["content"])
                changed_file_paths.append(created["path"])

            print(f"변경된 파일 경로들: {changed_file_paths}")
            print(f"파일 변경사항이 반영되었습니다. : {execution_result_path}")

            if not get_user_confirm_input(f"{task['id']} Review를 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            print(f"4️⃣  Reviewing task: {task['id']}")

            changed_file_contents = build_app_file_content_list(changed_file_paths)

            review_result = reviewer_agent(task, changed_file_contents)
            review_result_path = project_dir / f"04_review_{task['id']}.json"
            write_json_file(review_result_path, review_result)

            print(f"리뷰가 생성되었습니다. : {review_result_path}")

    except Exception as e:
        print("❌ 워크플로우 실행 중 오류 발생")
        print(f"오류 메시지: {e}")
        print("=" * 50)
        print(traceback.format_exc())
