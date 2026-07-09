from pathlib import Path
from app.cli import CommandLoop
from app.service import ReportService
from app.store import DataStore


if __name__ == "__main__":
    reports_file = Path("data/reports.json")
    data_store = DataStore(reports_file)
    report_service = ReportService(data_store)
    command_loop = CommandLoop(report_service)
    command_loop.run()

