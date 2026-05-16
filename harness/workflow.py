from agents.planner import planner_agent
from agents.task_decomposer import task_decomposer_agent
from agents.executor import executor_agent
from agents.reviewer import reviewer_agent
from tools.file_explorer import (
    apply_app_changes,
    build_app_file_content_list,
    load_json_file,
    write_json_file,
)


def run_workflow(project_dir):

    try:
        print("1️⃣  Planning...")
        target = load_json_file(project_dir / "target.json")
        related_file_contents = build_app_file_content_list(
            target.get("file_paths", [])
        )

        plan = planner_agent(target, related_file_contents)
        write_json_file(project_dir / "01_plan.json", plan)

        print("2️⃣  Decomposing tasks...")

        tasks = task_decomposer_agent(plan)
        write_json_file(project_dir / "02_tasks.json", tasks)

        print("3️⃣  Executing...")

        for task in tasks["tasks"]:
            related_file_contents = build_app_file_content_list(
                task.get("related_file_paths", [])
            )
            execution_result = executor_agent(task, related_file_contents)
            write_json_file(
                project_dir / f"03_execution_{task['id']}.json", execution_result
            )
            changed_file_paths = []
            for modified in execution_result.get("modified_files", []):
                apply_app_changes(modified["path"], modified["content"])
                changed_file_paths.append(modified["path"])

            for created in execution_result.get("created_files", []):
                apply_app_changes(created["path"], created["content"])
                changed_file_paths.append(created["path"])

            print("4️⃣  Reviewing...")

            changed_file_contents = build_app_file_content_list(changed_file_paths)
            review_result = reviewer_agent(task, changed_file_contents)
            write_json_file(project_dir / f"04_review_{task['id']}.json", review_result)

    except Exception as e:
        print("❌ 워크플로우 실행 중 오류 발생")
        print(e)
