from docx import Document

class WordDocParser:
    def __init__(self, file_path):
        """ Initialize with the file path """
        self.file_path = file_path
        try:
            self.document = Document(file_path)
        except PermissionError:
            raise PermissionError(f"Cannot open the file {file_path}. Check read-only permissions.")
        
        self.data = {
            "headings": [],
            "bold_phrases": [],
            "italic_phrases": []
        }

    def extract_headings(self):
        """ Extract all headings based on paragraph style """
        for paragraph in self.document.paragraphs:
            if paragraph.style.name.startswith('Heading'):
                self.data["headings"].append({
                    "text": paragraph.text.strip(),
                    "level": paragraph.style.name
                })

    def extract_formatted_phrases(self):
        """ Extract phrases that are fully bold or italic """
        for paragraph in self.document.paragraphs:
            bold_phrase, italic_phrase = [], []

            for run in paragraph.runs:
                word = run.text.strip()

                # Check for bold phrases
                if run.bold:
                    bold_phrase.append(word)
                elif bold_phrase:
                    # Save collected bold phrase when formatting ends
                    self.data["bold_phrases"].append(" ".join(bold_phrase))
                    bold_phrase = []

                # Check for italic phrases
                if run.italic:
                    italic_phrase.append(word)
                elif italic_phrase:
                    # Save collected italic phrase when formatting ends
                    self.data["italic_phrases"].append(" ".join(italic_phrase))
                    italic_phrase = []

            # Add remaining phrases at the end of the paragraph
            if bold_phrase:
                self.data["bold_phrases"].append(" ".join(bold_phrase))
            if italic_phrase:
                self.data["italic_phrases"].append(" ".join(italic_phrase))

    def parse_document(self):
        """ Main method to extract all relevant data """
        self.extract_headings()
        self.extract_formatted_phrases()
        return self.data