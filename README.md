# snellium_test
<!-- python 3.14.3 -->
The program is a CLI tool that allows users to manage and retrieve reports associated with different authors. It provides functionalities to add or copy reports, list authors, and retrieve reports by author name.

It uses a JSON file to store the authors and their associated reports.
The JSON file is loaded once when the program starts, and any changes made to the reports are saved back to the file. It uses a lookup dictionary with composite keys (author_name, report_filename) to allow quick access to the data without reading the entire file for each operation.

Overview of the program:
- main.py: The entry point. It initializes the objects and runs the command loop.
- cli.py: Class that handles user input to manage the report records.
- services.py: Class that provides methods to save/copy and retrieve reports.
- store.py: Class that handles reading and writing the JSON file.

