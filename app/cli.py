from pathlib import Path

from app.service import ReportService


class CommandLoop:
    def __init__(self, report_service: ReportService):
        self.report_service = report_service

    
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
                self.report_service.add_report(Path(args[1]), args[2])
                print(f"Added report for author {args[2]}")
            case "authors":
                for author_name in self.report_service.list_authors():
                    print(author_name)
            case "reports":
                for report_filename in self.report_service.list_reports_by_author(args[1]):
                    print(report_filename)
            case "save":
                self.report_service.copy_report(args[1], args[2], args[3])
                print(f"Report successfully copied to {args[3]}")

