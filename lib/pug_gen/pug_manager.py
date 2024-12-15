from pathlib import Path

class PugManager:
    def __init__(self, output_path='output/', filename='main'):
        """
        Initializes a PugManager object.

        Args:
            output_path: The path to the output directory. Defaults to 'output/'.
            filename: The name of the output file. Defaults to 'main'.
        """
        self.filename = f"{output_path}/{filename}/index.pug"
        Path(self.filename).parent.mkdir(parents=True, exist_ok=True) 

        with open(self.filename, 'w') as f:
            f.writelines([
                'doctype html\n', 
                'html(lang=\'en\')\n',
                '\thead\n',
                '\t\tmeta(charset="UTF-8")\n',
                '\t\tmeta(name="viewport" content="width=device-width, initial-scale=1.0")\n',
                '\tbody\n'
            ])

    def __add_meta_tags(self, tag_name, content, properties=["og", "twitter"]):
        """
        Adds meta tags to the Pug file.

        Args:
            tag_name: The name of the meta tag (e.g., "title", "description", "image").
            content: The content for the meta tag.
            properties: A list of property names (e.g., "og", "twitter").
        """
        lines = []
        for property in properties:
            lines.append(f'meta(name="{tag_name}" property="{property}:{tag_name}" content="{content}")\n')
        lines = self.__update_list_index(lines, 2) 
        new_lines = self.__find_location_in_file('head', lines, after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def addTitle(self, title: str):
        """Adds a title meta tag to the Pug file."""
        self.__add_meta_tags("title", title)

    def addDescription(self, description: str):
        """Adds a description meta tag to the Pug file."""
        self.__add_meta_tags("description", description)

    def addImage(self, image: str):
        """Adds an image meta tag to the Pug file."""
        self.__add_meta_tags("image", image)

    def addMeta(self, meta_tags: dict):
        """Adds custom meta tags to the Pug file."""
        for key, value in meta_tags.items():
            self.__add_meta_tags(key, value) 

    def __update_list_index(self, lines, index_offset):
        """
        Updates the index of lines in the Pug file.

        Args:
            lines: A list of lines to be inserted.
            index_offset: The offset to be added to the line indices.

        Returns:
            A list of lines with updated indices.
        """
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\t', '\t' * (index_offset + 1))
        return lines

    def __find_location_in_file(self, tag, lines, after):
        """
        Finds the appropriate location to insert lines in the Pug file.

        Args:
            tag: The tag to find (e.g., "head").
            lines: A list of lines to be inserted.
            after: The index of the line after which to insert the new lines.

        Returns:
            A list of lines with the new lines inserted.
        """
        with open(self.filename, 'r') as f:
            file_lines = f.readlines()

        for i, line in enumerate(file_lines):
            if line.strip() == tag:
                file_lines[i+after:i+after] = lines
                break

        return file_lines
    
    def __update_list_index(self, lines, index_offset):
        """
        Updates the index of lines in the Pug file.

        Args:
            lines: A list of lines to be inserted.
            index_offset: The offset to be added to the line indices.

        Returns:
            A list of lines with updated indices.
        """
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\t', '\t' * (index_offset + 1))
        return lines

    def __find_location_in_file(self, tag, lines, after=None):
        """
        Finds the appropriate location to insert lines in the Pug file.

        Args:
            tag: The tag to find (e.g., "head").
            lines: A list of lines to be inserted.
            after: The index of the line after which to insert the new lines (optional).

        Returns:
            A list of lines with the new lines inserted.
        """
        with open(self.filename, 'r') as f:
            file_lines = f.readlines()

        for i, line in enumerate(file_lines):
            if line.strip() == tag:
                if after is not None:
                    i += after + 1
                file_lines[i:i] = lines
                break

        return file_lines

    def __append_newline_char(self, lines):
        """
        Appends a newline character to each line in the list.

        Args:
            lines: A list of lines.

        Returns:
            A list of lines with a newline character appended to each.
        """
        return [line + '\n' for line in lines]

    def __add_css_link(self, parent=False, css_filename='style.css'):
        """
        Adds a CSS link to the head of the Pug file.

        Args:
            parent: If True, the link will reference the CSS file in the parent directory.
            css_filename: The name of the CSS file.
        """
        link = f'link(rel="stylesheet" href="{("/../" if parent else "/")}{css_filename}")\n'
        lines = self.__update_list_index([link], 2)
        new_lines = self.__find_location_in_file('head', lines, after=self.elements['head'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)

    def __add_javascript_link(self, parent=False, js_filename='main.js'):
        """
        Adds a JavaScript link to the body of the Pug file.

        Args:
            parent: If True, the link will reference the JS file in the parent directory.
            js_filename: The name of the JS file.
        """
        link = f'script(type="text/javascript" src="{("/../" if parent else "/")}{js_filename}")\n'
        lines = self.__update_list_index([link], 2)
        new_lines = self.__find_location_in_file('body', lines, after=self.elements['body'])
        with open(self.filename, 'w') as f:
            f.writelines(new_lines)