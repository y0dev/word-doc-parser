from docx import Document

class WordDocParser:
    """
    This class parses a Word document (.docx) and extracts specific data.
    """

    def __init__(self, file_path):
        """
        Initializes the WordDocParser object with the file path.

        Args:
            file_path (str): The path to the Word document (.docx) file.

        Raises:
            PermissionError: If the file cannot be opened due to permission issues.
        """
        self.file_path = file_path
        try:
            self.document = Document(file_path)
        except PermissionError:
            raise PermissionError(f"Cannot open the file {file_path}. Check read-only permissions.")
        self.__desc_start = False
        self.data = {
            "metadata": {"id":"","type":"","title":"", "description":""},
            "headings": [],
            "paragraphs": []
        }

    def extract_headings(self):
        """
        Extracts all headings from the document based on their paragraph style
        and stores them in a hierarchical structure with nested paragraphs.

        Iterates through each paragraph. If the paragraph style indicates a heading,
        a new dictionary entry is created with heading text, level, and an empty
        "paragraphs" list to hold nested content. Otherwise, it extracts formatted
        phrases and lists within the paragraph and adds them to a separate dictionary
        representing the paragraph data. This dictionary is then appended either to
        the current heading's "paragraphs" list (if inside a heading) or to the main
        "paragraphs" list in the `data` dictionary.
        """
        current_heading = None
        for paragraph in self.document.paragraphs:
            if not paragraph.text: continue
            if self.__desc_start:
                self.data["metadata"]["description"] = paragraph.text.lower().strip()
                self.__desc_start = False
                continue
            if paragraph.text.lower().startswith('article-id'):
                self.data["metadata"]["id"] = paragraph.text.lower().split('=')[1].strip()
                continue
            elif paragraph.text.lower().startswith('article-type'):
                self.data["metadata"]["type"] = paragraph.text.lower().split('=')[1].strip()
                continue
            elif paragraph.text.lower().startswith('article-title'):
                self.data["metadata"]["title"] = paragraph.text.lower().split('=')[1].strip()
                continue
            elif paragraph.text.lower().startswith('description'):
                self.__desc_start = True
                continue

            if paragraph.style.name.startswith('Heading'):
                current_heading = {
                    "text": paragraph.text.strip(),
                    "level": paragraph.style.name,
                    "paragraphs": []
                }
                self.data["headings"].append(current_heading)
            else:
                paragraph_data = {
                    "text": paragraph.text.strip(),
                    "bold_phrases": [],
                    "italic_phrases": [],
                    "lists": []
                }
                self.extract_formatted_phrases(paragraph, paragraph_data)
                self.extract_lists(paragraph, paragraph_data)
                if current_heading:
                    current_heading["paragraphs"].append(paragraph_data)
                else:
                    self.data["paragraphs"].append(paragraph_data)

    def extract_formatted_phrases(self, paragraph, paragraph_data):
        """
        Extracts phrases that are entirely bold or italic within a paragraph.

        Iterates through each text run (formatted text segment) in the paragraph.
        Maintains temporary lists for ongoing bold and italic phrases. It only adds
        a phrase to the corresponding list in the `paragraph_data` dictionary
        ("bold_phrases" or "italic_phrases") when the phrase ends (no longer bold/italic).
        This ensures that only complete formatted phrases are captured.

        Args:
            paragraph (docx.paragraph.Paragraph): A paragraph object from the Word document.
            paragraph_data (dict): A dictionary to store extracted data for the current paragraph.
        """
        bold_phrase, italic_phrase = [], []

        for run in paragraph.runs:
            word = run.text.strip()

            if run.bold:
                bold_phrase.append(word)
            elif bold_phrase:
                paragraph_data["bold_phrases"].append(" ".join(bold_phrase))
                bold_phrase = []

            if run.italic:
                italic_phrase.append(word)
            elif italic_phrase:
                paragraph_data["italic_phrases"].append(" ".join(italic_phrase))
                italic_phrase = []

        if bold_phrase:
            paragraph_data["bold_phrases"].append(" ".join(bold_phrase))
        if italic_phrase:
            paragraph_data["italic_phrases"].append(" ".join(italic_phrase))

    def extract_lists(self, paragraph, paragraph_data):
        """
        Extracts numbered and bulleted lists within a paragraph.

        Checks if the paragraph style indicates a list ("List Paragraph"). If so,
        it extracts the list text and its indent level. The indent level helps
        identify the nesting of lists within the document. The extracted information
        is then added as a dictionary to the "lists" list within the `paragraph_data` dictionary.

        Args:
            paragraph (docx.paragraph.Paragraph): A paragraph object from the Word document.
            paragraph_data (dict): A dictionary to store extracted data for the current paragraph.
        """
        if paragraph.style.name in ['List Paragraph']: 
            list_text = paragraph.text.strip()
            indent_level = paragraph.paragraph_format.left_indent.pt if paragraph.paragraph_format.left_indent else 0
            paragraph_data["lists"].append({
                "text": list_text,
                "indent_level": indent_level
            })

    def parse_document(self):
        """
        The main method to initiate the parsing process.

        Calls all the individual extraction methods like `extract_headings`,
        `extract_formatted_phrases`, and `extract_lists` to extract the desired data.
        Returns the extracted data stored in the `data` dictionary.

        Returns:
            dict: A dictionary containing extracted information from the document.
        """
        self.extract_headings()
        return self.data
