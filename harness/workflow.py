import traceback
from pathlib import Path

from agents.executor import executor_agent
from agents.planner import planner_agent
from agents.reviewer import reviewer_agent
from agents.task_decomposer import task_decomposer_agent
from tools.cli import get_user_confirm_input, run_command
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

        plan_result = planner_agent(target, related_file_contents)
        write_json_file(project_dir / "01_plan.json", plan_result)

        print("프로젝트 설계 문서가 생성되었습니다. : " + "01_plan.json")
        if not get_user_confirm_input("Task decomposition을 진행할까요?"):
            print("🟥 워크플로우가 중단되었습니다.")
            return

        print("2️⃣  Decomposing tasks...")

        decompose_result = task_decomposer_agent(plan_result)
        write_json_file(project_dir / "02_tasks.json", decompose_result)

        print("Task 분해가 완료되었습니다. : " + "02_tasks.json")

        tasks = decompose_result.get("tasks", [])
        for task in tasks:
            if not get_user_confirm_input(f"{task['id']} Execution을 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            print(f"3️⃣  Executing task: {task['id']}")

            related_files = list(task.get("related_files", []))
            for task_id in task.get("dependencies", []):
                parent_task = next(
                    (task for task in tasks if task["id"] == task_id),
                    None,
                )
                if parent_task:
                    related_files.extend(parent_task.get("related_files", []))

            related_file_contents = build_app_file_content_list(related_files)

            execution_result = executor_agent(task, related_file_contents)
            execution_result_path = project_dir / f"03_execution_{task['id']}.json"
            write_json_file(execution_result_path, execution_result)

            changed_files = []

            for modified in execution_result.get("modified_files", []):
                print(f"변경된 파일: {modified['path']}")
                apply_app_changes(modified["path"], modified["content"])
                changed_files.append(modified["path"])

            for created in execution_result.get("created_files", []):
                print(f"생성된 파일: {created['path']}")
                apply_app_changes(created["path"], created["content"])
                changed_files.append(created["path"])

            print(f"변경된 파일 경로들: {changed_files}")
            print(f"파일 변경사항이 반영되었습니다. : {execution_result_path}")

            if not get_user_confirm_input("검증을 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            while True:
                failed_validations = run_project_validations(changed_files)

                if not failed_validations:
                    print("✅ 모든 검증을 통과했습니다.")
                    break

                print(f"❌ 검증 실패: {', '.join(failed_validations)}")
                retry = get_user_confirm_input(
                    "검증을 재시도하려면 Y, 건너뛰려면 N을 입력하세요."
                )

                if not retry:
                    print("검증을 수동 건너뛰기하였습니다.")
                    break

            if not get_user_confirm_input(f"{task['id']} Review를 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            while True:
                print(f"4️⃣  Reviewing task: {task['id']}")

                changed_file_contents = build_app_file_content_list(changed_files)

                review_result = reviewer_agent(task, changed_file_contents)
                review_result_path = project_dir / f"04_review_{task['id']}.json"
                write_json_file(review_result_path, review_result)

                print(f"리뷰가 생성되었습니다. : {review_result_path}")

                if review_result["result"] == "passed":
                    print("✅ 리뷰를 통과했습니다.")
                    break

                retry = get_user_confirm_input("리뷰를 다시 요청할까요? (Y/N)")

                if not retry:
                    print("리뷰를 수동 건너뛰기하였습니다.")
                    break

    except Exception as e:
        print("❌ 워크플로우 실행 중 오류 발생")
        print(f"오류 메시지: {e}")
        print("=" * 50)
        print(traceback.format_exc())


def run_project_validations(changed_files):
    app_dir = "app"

    failed_validations = []

    if "package.json" in changed_files:
        success = run_command("npm install", app_dir)
        if not success:
            failed_validations.append("install")
    else:
        pass

    try:
        package_json = load_json_file(f"{app_dir}/package.json")
        scripts = package_json.get("scripts", {})
    except Exception:
        scripts = {}

    if "typecheck" in scripts:
        success = run_command("npm run typecheck", app_dir)
        if not success:
            failed_validations.append("typecheck")
    else:
        pass

    if "build" in scripts:
        success = run_command("npm run build", app_dir)
        if not success:
            failed_validations.append("build")
    else:
        failed_validations.append("build")

    return failed_validations
