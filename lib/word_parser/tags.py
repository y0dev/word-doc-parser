class Tags:
    def __init__(self, doc_type):
        self.doc_type = doc_type.lower()
        self.tag_list = []
        self.__generate_tag_list()
        print(doc_type)

    def get_tag_list(self):
        return self.tag_list

    def __generate_tag_list(self):
        """
        Generates a list of tags based on the document type.

        This function dynamically populates the `tag_list` attribute with relevant tags 
        depending on the value of `self.doc_type`.

        """
        if self.doc_type == "theology":
            self.tag_list.extend(["Theology", "God", "Gospel", "Reformed"])
        elif self.doc_type == "covenant":
            self.tag_list.extend(["Christ", "Covenant", "Reformed", "Gospel"])
        elif self.doc_type == "thankful":
            self.tag_list.extend(["Christ", "Salvation", "Love", "Thankful"])
        elif self.doc_type == "health":
            self.tag_list.extend(["Health", "Fitness"])
        elif self.doc_type in ["tech", "technology"]:
            self.tag_list.extend(["Technology", "Engineer"])
        elif self.doc_type in ["algo", "algorithm"]:
            self.tag_list.extend(["Data Structures", "Algorithms", "Tech Interview"])
        elif self.doc_type == "system design":
            self.tag_list.extend(["System Design", "Technology", "Tech Interview"])
        elif self.doc_type == "embedded":
            self.tag_list.extend(["Embedded Systems", "Microcontrollers", "IoT", "C", "C++", "RTOS"])
        else:
            self.tag_list.extend(["Template", "Info", "Beginner"])
