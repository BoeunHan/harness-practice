from agents.planner import planner_agent
from tools.file_explorer import (
    build_file_content_list,
    load_json_file,
    write_json_file,
)


def run_workflow(project_dir):

    try:
        print("1️⃣  Planning...")
        target = load_json_file(project_dir / "target.json")
        related_file_contents = build_file_content_list(target.get("file_paths", []))

        plan = planner_agent(target, related_file_contents)

        print(plan)
        write_json_file(project_dir / "plan.json", plan)
        print("2️⃣  Decomposing tasks...")

        print("3️⃣  Executing...")

        print("4️⃣  Reviewing...")

    except Exception as e:
        print("❌ 워크플로우 실행 중 오류 발생")
        print(e)
