import json
from pathlib import Path


class DataStore:
    def __init__(self, data_file):
        self.data_file = Path(data_file)

    
    def load_records(self):
        # load records from JSON file and return as list of dicts
        if not self.data_file.exists():
            return []

        with self.data_file.open("r", encoding="utf-8") as file_handle:
            raw_data = json.load(file_handle)

        records = []
        authors_mapping = raw_data.get("authors", {})

        for author_name, entries in authors_mapping.items():
            for entry in entries:
                records.append(
                    {
                        "author_name": author_name,
                        "filename": entry["filename"],
                        "original_path": Path(entry["path"]),
                    }
                )

        return records

    
    def save_records(self, records):
        # save records to JSON file, grouped by author
        grouped_records = {}

        for record in records:
            author_name = record["author_name"]
            grouped_records.setdefault(author_name, []).append(record)

        serialized_data = {"authors": {}}

        for author_name, report_records in grouped_records.items():
            serialized_data["authors"][author_name] = [
                {
                    "filename": record["filename"],
                    "path": str(record["original_path"]),
                }
                for record in sorted(report_records, key=lambda rec: rec["filename"])
            ]

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file_handle:
            json.dump(serialized_data, file_handle, ensure_ascii=False, indent=4)
    