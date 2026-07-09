import json
from pathlib import Path

from app.service import ReportService


class CommandLoop:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service
        self.report_file = Path("data/reports.json")

    
    def run(self):
        print("Welcome in report management system!")
        print("Loading database... done.")
        print("Please enter a command:")

        while True:
            user_input = input("> ").strip()
            if user_input == "exit":
                break
            self.handle_command(user_input)

    
    def handle_command(self, user_input: str):
        args = [arg.strip() for arg in user_input.split(",")]
        command_name = args[0]

        match command_name:
            case "add":
                report_file, author_name = Path(args[1]), args[2]
                report_path = Path("data/reports.json")
                content = {}

                if report_path.exists():
                    with open(report_path, "r", encoding="utf-8") as f:
                        content = json.load(f)

                authors = content.get("authors", {})
                new_entry = {
                    "filename": report_file.name,
                    "path": str(report_file)
                }
                if new_entry not in authors.get(author_name, []):
                    authors.setdefault(author_name, [])
                    authors[author_name].append(new_entry)
                    content["authors"] = authors

                    report_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(report_path, "w", encoding="utf-8") as f:
                        json.dump(content, f, ensure_ascii=False, indent=4)

                    print(f"Added report for author {author_name}")

            
            case "authors":
                for author_name in self.report_service.list_authors():
                    print(author_name)
            
            case "reports":
                author_name = args[1]
                for report_filename in self.report_service.list_reports_by_author(author_name):
                    print(report_filename)
            
            case "save":
                author_name = args[1]
                report_filename = args[2]
                destination_path_text = args[3]

                self.report_service.copy_report(
                    author_name,
                    report_filename,
                    destination_path_text,
                )
                print(f"Report successfully copied to {destination_path_text}")
            
            case _:
                print("Unknown command")

