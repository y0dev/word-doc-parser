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
            raise PermissionError(
                f"Cannot open the file {file_path}. Check read-only permissions."
            )

        self.data = {
            "headings": [],
            "bold_phrases": [],
            "italic_phrases": [],
            "lists": [],
            "paragraphs": []
        }

    def extract_paragraphs(self):
        """
        Extracts all paragraphs from the document and stores them as plain text.

        Iterates through each paragraph in the document and appends its stripped text
        (removing leading/trailing whitespace) to the "paragraphs" list within the `data` dictionary.
        """
        for paragraph in self.document.paragraphs:
            self.data["paragraphs"].append(paragraph.text.strip())

    def extract_headings(self):
        """
        Extracts all headings from the document based on their paragraph style.

        Iterates through each paragraph and checks if its style name starts with
        "Heading". If so, it adds an entry to the "headings" list in the `data`
        dictionary with the heading text and its level (style name).
        """
        for paragraph in self.document.paragraphs:
            if paragraph.style.name.startswith("Heading"):
                self.data["headings"].append(
                    {
                        "text": paragraph.text.strip(),
                        "level": paragraph.style.name,
                    }
                )

    def extract_formatted_phrases(self):
        """
        Extracts phrases that are fully bold or italic within the document.

        Iterates through each paragraph and its runs (text segments with formatting).
        It keeps track of ongoing bold and italic phrases and adds them to the
        corresponding lists in the `data` dictionary ("bold_phrases" and "italic_phrases")
        only when the phrase ends (meaning no longer bold/italic).
        """
        for paragraph in self.document.paragraphs:
            bold_phrase, italic_phrase = [], []

            for run in paragraph.runs:
                word = run.text.strip()

                # Check for bold phrases
                if run.bold:
                    bold_phrase.append(word)
                elif bold_phrase:
                    self.data["bold_phrases"].append(" ".join(bold_phrase))
                    bold_phrase = []

                # Check for italic phrases
                if run.italic:
                    italic_phrase.append(word)
                elif italic_phrase:
                    self.data["italic_phrases"].append(" ".join(italic_phrase))
                    italic_phrase = []

            # Add any remaining bold or italic phrases at the end of the paragraph
            if bold_phrase:
                self.data["bold_phrases"].append(" ".join(bold_phrase))
            if italic_phrase:
                self.data["italic_phrases"].append(" ".join(italic_phrase))

    def extract_lists(self):
        """
        Extracts numbered and bulleted lists from the document.

        Iterates through paragraphs and checks if their style name indicates a list.
        If so, it extracts the list text and its indent level and adds them to the
        "lists" list in the `data` dictionary.
        """
        for paragraph in self.document.paragraphs:
            if paragraph.style.name in ["List Paragraph"]:
                list_text = paragraph.text.strip()
                indent_level = (
                    paragraph.paragraph_format.left_indent.pt
                    if paragraph.paragraph_format.left_indent
                    else 0
                )
                self.data["lists"].append(
                    {"text": list_text, "indent_level": indent_level}
                )

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
        self.extract_formatted_phrases()
        self.extract_lists()
        self.extract_paragraphs()
        return self.data