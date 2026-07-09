import json
from pathlib import Path


class MetadataStore:
    def __init__(self, metadata_file):
        self.metadata_file = metadata_file

    
    def load_records(self):
        if not self.metadata_file.exists():
            return []

        with self.metadata_file.open("r", encoding="utf-8") as file_handle:
            raw_data = json.load(file_handle)

        loaded_records = []
        authors_mapping = raw_data.get("authors", {})

        for author_name, report_entries in authors_mapping.items():
            for report_entry in report_entries:
                loaded_records.append(
                    {
                        "filename": report_entry["filename"],
                        "original_path": Path(report_entry["path"]),
                        "author_name": author_name,
                    }
                )

        return loaded_records

    
    def save_records(self, records):
        grouped_records = {}

        for record in records:
            author_name = record["author_name"]

            if author_name not in grouped_records:
                grouped_records[author_name] = []

            grouped_records[author_name].append(record)

        serialized_data = {"authors": {}}

        for author_name in grouped_records:
            sorted_records = sorted(
                grouped_records[author_name],
                key=lambda record: record["filename"],
            )

            serialized_data["authors"][author_name] = []

            for record in sorted_records:
                serialized_data["authors"][author_name].append(
                    {
                        "filename": record["filename"],
                        "path": str(record["original_path"]),
                    }
                )

        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)

        with self.metadata_file.open("w", encoding="utf-8") as file_handle:
            json.dump(serialized_data, file_handle, indent=2)
