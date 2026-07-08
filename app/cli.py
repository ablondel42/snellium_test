class CommandLoop:
    def __init__(self, report_service):
        self.report_service = report_service

    def run(self):
        print("Welcome in report management system!")
        print("Loading database... done.")
        print("Please enter a command:")

        while True:
            raw_command = input("> ").strip()

            if raw_command == "exit":
                break

            self._handle_command(raw_command)

    def _handle_command(self, raw_command):
        parts = [part.strip() for part in raw_command.split(",")]
        command_name = parts[0]

        if command_name == "add":
            report_path_text = parts[1]
            author_name = parts[2]
            self.report_service.add_report(report_path_text, author_name)
            return

        if command_name == "authors":
            for author_name in self.report_service.list_authors():
                print(author_name)
            return

        if command_name == "reports":
            author_name = parts[1]
            for report_filename in self.report_service.list_reports_by_author(author_name):
                print(report_filename)
            return

        if command_name == "save":
            author_name = parts[1]
            report_filename = parts[2]
            destination_path_text = parts[3]

            self.report_service.save_report_copy(
                author_name,
                report_filename,
                destination_path_text,
            )
            print(f"Report successfully copied to {destination_path_text}")
            return
