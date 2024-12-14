class Image:
    def __init__(self, doc_type):
        self.doc_type = doc_type.lower()
        self.image = {}
        self.__generate_image()

    def __generate_image(self):
        if self.doc_type in ["theology", "covenant"]:
            self.image = {"name": "images/bible-icon.png", "alt": "bible-icon"}
        elif self.doc_type == "thankful":
            self.image = {"name": "images/thankful.png", "alt": "thankful-icon"}
        elif self.doc_type == "family":
            self.image = {"name": "images/family.png", "alt": "family-image"}
        elif self.doc_type == "health":
            self.image = {"name": "images/heart_strength.png", "alt": "health-img"}
        elif self.doc_type in ["code", "tech", "technology", "system design"]:
            self.image = {"name": "images/web-dev.png", "alt": "web-dev-img"}
        elif self.doc_type in ["algo", "algorithm"]:
            self.image = {"name": "images/algorithm.png", "alt": "algo-img"}
        elif self.doc_type == "docker":
            self.image = {"name": "images/docker.png", "alt": "docker-image"}
        elif self.doc_type == "jenkins":
            self.image = {"name": "images/jenkins.png", "alt": "jenkins-image"}
        else:
            self.image = {"name": "images/image.png", "alt": "image-title"}

    def get_image(self):
        return self.image
