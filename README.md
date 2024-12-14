# Word Doc Parser - Automate Your Document Processing

This Python script provides a user-friendly way to parse and process Word documents (.docx format).

## Key Features

- **User-friendly interface:** Select the .docx file you want to parse from a directory.
- **Customizable output:** Generate JSON files with extracted information based on your needs.
- **Flexibility:** Easily adapt the code for different parsing functionalities.
- **Robust error handling:** Handles potential issues like missing files or invalid input.

## How to Use

**Prerequisites:**

- Python 3.x installed on your system.
- The `python-docx` library installed: `pip install python-docx`

**Steps:**

1. **Clone the Script:**
   - Clone the Git repository containing the scripts.
2. **Set Up the Input Directory:**
   - Create a directory containing the Word documents you want to process.
3. **Run the Application:**
   - Open a terminal or command prompt.
   - Navigate to the directory containing the script files (e.g., `cd word-doc-parser`).
   - Run the script using: `python main.py`
   - The script will prompt you to select a document from the input directory.
4. **Run Tests (Optional):**

   - To ensure the script is working correctly, you can run unit tests:

     ```bash
     python -m unittest discover tests
     ```

     This will execute the tests located in the `tests` directory (assuming you have one).

## Future Enhancements

- Support for additional document formats (e.g., PDF).
- Advanced parsing capabilities (e.g., extracting tables, images).
- Integration with other tools or workflows.

This script serves as a starting point for automating your Word document processing tasks. Feel free to modify and extend it to suit your specific needs!
