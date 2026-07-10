# snellium_test
<!-- "python 3.14.3" -->
<!-- "python3 main.py" to start the program -->

The program is a CLI tool that allows users to manage and retrieve reports written by different authors. It provides functions to add or copy reports, list authors, and retrieve reports.

It uses a JSON file to persist the authors and their associated reports.
The JSON file is loaded once when the program starts, and any changes made to the reports are saved back to the file.

It also uses 2 dictionaries to store the data in memory:
- `self.authors_to_reports`: Maps author names to lists of their reports.
- `self.report_lookup`: Maps (author_name, report_filename) keys to the corresponding report records to do faster lookups and retrievals. (Example: avoid scanning the entire list of reports for an author when looking for a specific report to copy or retrieve.)

Overview of the classes and files:
- main.py: The entry point. It initializes the objects and runs the command loop.
- cli.py: Class that handles user input to manage the report records.
- services.py: Class that provides methods to save/copy and retrieve reports.
- store.py: Class that handles reading and writing the JSON file.

