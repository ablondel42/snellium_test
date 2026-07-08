from pathlib import Path
from app.cli import CommandLoop
from app.service import ReportService
from app.store import MetadataStore


if __name__ == "__main__":
    metadata_file = Path("data/reports.json")
    metadata_store = MetadataStore(metadata_file)
    report_service = ReportService(metadata_store)
    command_loop = CommandLoop(report_service)
    command_loop.run()

