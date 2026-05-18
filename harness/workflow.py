import traceback
from pathlib import Path

from agents.executor import run_executor_agent
from agents.planner import run_planner_agent
from agents.reviewer import run_reviewer_agent
from agents.task_decomposer import run_task_decomposer_agent
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

        run_planner_agent(project_dir)

        print("프로젝트 설계 문서가 생성되었습니다. : " + "01_plan.json")
        if not get_user_confirm_input("Task decomposition을 진행할까요?"):
            print("🟥 워크플로우가 중단되었습니다.")
            return

        print("2️⃣  Decomposing tasks...")

        run_task_decomposer_agent(project_dir)

        print("Task 분해가 완료되었습니다. : " + "02_tasks.json")

        tasks = load_json_file(project_dir / "02_tasks.json").get("tasks", [])

        for task in tasks:
            if not get_user_confirm_input(f"{task['id']} Execution을 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            print(f"3️⃣  Executing task: {task['id']}")

            run_executor_agent(project_dir, task["id"])

            print(f"${task['id']} 구현 작업이 완료되었습니다.")

            if not get_user_confirm_input("검증을 진행할까요?"):
                print("🟥 워크플로우가 중단되었습니다.")
                return

            changed_files = load_json_file(
                project_dir / f"03_{task['id'].split('_')[0]}_execution.json"
            ).get("modified_files", []) + load_json_file(
                project_dir / f"03_{task['id'].split('_')[0]}_execution.json"
            ).get("created_files", [])

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

                run_reviewer_agent(project_dir, task["id"])
                review_result = load_json_file(
                    project_dir / f"04_{task['id'].split('_')[0]}_review.json"
                )

                print(f"${task['id']} 코드 리뷰가 완료되었습니다.")

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
    print(changed_files)
    if "package.json" in changed_files or "app/package.json" in changed_files:
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
