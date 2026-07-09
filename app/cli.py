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


    def read_records(self):
        with open(self.report_file, "r", encoding="utf-8") as f:
            return json.load(f)
        # return content
    

    def write_records(self, records):
        content = { "authors": records }
        self.report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.report_file, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)


    def add_report(self, report_path: Path, author_name: str):
        content = self.read_records()
        authors = content.get("authors", {})
        new_entry = {
            "filename": report_path.name,
            "path": str(report_path)
        }
        if new_entry not in authors.get(author_name, []):
            authors.setdefault(author_name, [])
            authors[author_name].append(new_entry)
            content["authors"] = authors
            self.write_records(content["authors"])
            print(f"Added report for author {author_name}")


    def get_authors(self):
        if self.report_file.exists():
            content = self.read_records()
            for author_name in sorted(content.get("authors", {}).keys()):
                print(author_name)


    def get_reports_by_author(self, author_name: str):
        if self.report_file.exists():
            content = self.read_records()
            reports = content.get("authors", {}).get(author_name, [])
            for report in sorted(reports, key=lambda r: r["filename"]):
                print(report["filename"])


    def save_report(self, author_name: str, report_filename: str, destination_path_text: str):
        if self.report_file.exists():
            content = self.read_records()
            reports = content.get("authors", {}).get(author_name, [])
            report_entry = next((r for r in reports if r["filename"] == report_filename), None)
            if report_entry:
                original_path = Path(report_entry["path"])
                destination_path = Path(destination_path_text)
                destination_path.parent.mkdir(parents=True, exist_ok=True)
                with open(original_path, "rb") as src_file:
                    with open(destination_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
                print(f"Report successfully copied to {destination_path_text}")
            else:
                print(f"No report found for author {author_name} with filename {report_filename}")

    
    def handle_command(self, user_input: str):
        args = [arg.strip() for arg in user_input.split(",")]
        command_name = args[0]

        match command_name:
            case "add":
                self.add_report(Path(args[1]), args[2])
            
            case "authors":
                self.get_authors()

            case "reports":
                self.get_reports_by_author(args[1])
            
            case "save":
                self.save_report(args[1], args[2], args[3])
            
            case _:
                print("Unknown command")

