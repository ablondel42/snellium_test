from pathlib import Path
import shutil


class ReportService:
    def __init__(self, metadata_store):
        self.metadata_store = metadata_store
        self.authors_to_reports = {}
        self.report_lookup = {}
        self._load_existing_records()

    def _load_existing_records(self):
        loaded_records = self.metadata_store.load_records()
        self._rebuild_indexes(loaded_records)

    def _rebuild_indexes(self, records):
        self.authors_to_reports = {}
        self.report_lookup = {}

        for record in records:
            author_name = record["author_name"]
            filename = record["filename"]

            if author_name not in self.authors_to_reports:
                self.authors_to_reports[author_name] = []

            self.authors_to_reports[author_name].append(record)
            self.report_lookup[(author_name, filename)] = record

    def _all_records(self):
        all_records = []

        for report_records in self.authors_to_reports.values():
            all_records.extend(report_records)

        return all_records

    def add_report(self, report_path_text, author_name):
        report_path = Path(report_path_text)
        filename = report_path.name

        new_record = {
            "filename": filename,
            "original_path": report_path,
            "author_name": author_name,
        }

        lookup_key = (author_name, filename)

        if lookup_key in self.report_lookup:
            existing_reports = self.authors_to_reports[author_name]
            self.authors_to_reports[author_name] = [
                record
                for record in existing_reports
                if record["filename"] != filename
            ]

        if author_name not in self.authors_to_reports:
            self.authors_to_reports[author_name] = []

        self.authors_to_reports[author_name].append(new_record)
        self.report_lookup[lookup_key] = new_record

        self.metadata_store.save_records(self._all_records())

    def list_authors(self):
        return sorted(self.authors_to_reports.keys())

    def list_reports_by_author(self, author_name):
        author_reports = self.authors_to_reports.get(author_name, [])
        return sorted(record["filename"] for record in author_reports)

    def save_report_copy(self, author_name, report_filename, destination_path_text):
        record = self.report_lookup[(author_name, report_filename)]
        destination_path = Path(destination_path_text)

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(record["original_path"], destination_path)
