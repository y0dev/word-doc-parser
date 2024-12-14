import os
from lib.word_parser.word_doc_parser import WordDocParser
from utils.data_saver import DataSaver

def select_docx_file(input_dir):
  """
  Allows the user to select a .docx file from a given input directory.

  Args:
    input_dir: The path to the input directory.

  Returns:
    The path to the selected .docx file, or None if no .docx files are found.
  """

  docx_files = [f for f in os.listdir(input_dir) if f.endswith('.docx')]

  if not docx_files:
    print(f"No .docx files found in {input_dir}")
    return None

  print("Available .docx files:")
  for i, file_name in enumerate(docx_files):
    print(f"{i+1}. {file_name}")

  while True:
    try:
      choice = int(input("Enter the number of the file you want to select: "))
      if 1 <= choice <= len(docx_files):
        return os.path.join(input_dir, docx_files[choice - 1])
      else:
        print("Invalid choice. Please enter a number within the valid range.")
    except ValueError:
      print("Invalid input. Please enter a number.")

if __name__ == "__main__":

    # Example Usage
    input_dir = "input_docs"  # Replace with the actual input directory path
    selected_file = select_docx_file(input_dir)

    if selected_file:
      print(f"Selected file: {selected_file}") 
    else:
      exit(1)
      
    # Extract the filename without extension
    file_name, _ = os.path.splitext(os.path.basename(selected_file)) 

    # Create the output file path
    output_dir = "output/json"
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    output_file = os.path.join(output_dir, f"{file_name.lower()}.json") 

    print(f"Output file: {output_file}") 

    parser = WordDocParser(selected_file)
    extracted_data = parser.parse_document()

    saver = DataSaver(extracted_data, output_file)
    saver.save_to_json()
