from pathlib import Path
import shutil

from app.store import DataStore


class ReportService:
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.authors_to_reports = {}
        self.report_lookup = {}
        self.load_records()

    def load_records(self):
        records = self.data_store.load_records()
        self.authors_to_reports = {}
        self.report_lookup = {}

        for record in records:
            author_name = record["author_name"]
            filename = record["filename"]
            self.authors_to_reports.setdefault(author_name, []).append(record)
            self.report_lookup[(author_name, filename)] = record

    def _all_records(self):
        return [record for records in self.authors_to_reports.values() for record in records]

    def add_report(self, report_path, author_name):
        report_path = Path(report_path)
        filename = report_path.name
        new_record = {
            "author_name": author_name,
            "filename": filename,
            "original_path": report_path,
        }
        lookup_key = (author_name, filename)

        if lookup_key in self.report_lookup:
            self.authors_to_reports[author_name] = [
                record
                for record in self.authors_to_reports[author_name]
                if record["filename"] != filename
            ]

        self.authors_to_reports.setdefault(author_name, []).append(new_record)
        self.report_lookup[lookup_key] = new_record
        self.data_store.save_records(self._all_records())

    def list_authors(self):
        return sorted(self.authors_to_reports.keys())

    def list_reports_by_author(self, author_name):
        return sorted(record["filename"] for record in self.authors_to_reports.get(author_name, []))

    def copy_report(self, author_name, report_filename, destination_path_text):
        record = self.report_lookup[(author_name, report_filename)]
        destination_path = Path(destination_path_text)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(record["original_path"], destination_path)

