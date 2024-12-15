import utils.common_utils as cu

from .pug_manager import PugManager, indentList
import re


"""
    This is for 
"""

class Post_Generator:
    def __init__(self, title: str = 'Sample', description: str = 'Sample Description', post_type: str = 'article', json_obj: dict = {}) -> None:
        if len(json_obj) == 0:
            post_page_filename = 'main.pug'
        else:
            post_page_filename = json_obj['id']

        self.post_type = post_type
        if self.post_type.lower() == 'article':
            self.pm = PugManager(
                output_path='output/pug/articles', filename=f'{post_page_filename}')
        else:
            self.pm = PugManager(
                output_path='output/pug/notes', filename=f'{post_page_filename}')

        self.lines = []
        self.tags = []
        self.id_list = indentList()
        self.title = title
        self.description = description
        self.embedded = False
        self.languages = []
        self.code_script_added = False
        self.headshot = 'https://i.ibb.co/HY4dx9s/headshot.jpg'  # 'headshot.png'
        self.logo = '/images/logo.png'  # 'images/logo192.png'
        self.__getPostDetails(json_obj)
        self.__setupInitHead()
        self.__setupBody()

    def __getPostDetails(self, json_obj: dict):
        if len(json_obj) == 0:
            self.post_time = 'Thursday, October 6, 2022'
            self.post_info = {'date': 'Thursday, October 6, 2022'}
        else:
            from datetime import datetime
            self.post_info = json_obj
            self.title = self.post_info['title']
            # Add description
            if self.post_type.lower() == 'article':
                self.description = f'Blog post about {self.post_info["description"]}.'
            else:
                self.description = f'Note about {self.post_info["description"]}.'

            self.tags = self.post_info['tags']
            # Convert from js timestamp
            py_timestamp = int(self.post_info['date'])/1000.0
            # print(py_timestamp)
            self.post_info['date'] = datetime.fromtimestamp(
                py_timestamp).strftime("%A, %B %d, %Y")

    # Helper

    def __setupInitHead(self):
        meta_links = { 'twitter:card': 'summary_large_image', 'twitter:site': '@_yodev_',
                      'og:url': 'https://www.devontaereid.com', 'og:type': 'website'}
        self.pm.addTitle(self.title)
        self.pm.addDescription(self.description)
        self.pm.addIcon(logo_filename='/images/logo.png')
        self.pm.addImage(
            f'https://www.devontaereid.com/{self.post_info["image"]["name"]}')
        self.pm.addMeta(meta_links)
        self.pm.addCSS()

    def __addNavBar(self):
        self.lines.append(
            f'{self.id_list[0]}div#nav-bar.navbar.header-content--mini')
        self.lines.append(f'{self.id_list[1]}nav')
        self.lines.append(f'{self.id_list[2]}div.main-menu')
        self.lines.append(f'{self.id_list[3]}a.menu-branding(href="/")')
        self.lines.append(
            f'{self.id_list[4]}img.menu-branding(src="{self.logo}" alt="branding-logo")')
        self.lines.append(f'{self.id_list[4]}h3 Devontae Reid')

        # Menu List
        self.lines.append(f'{self.id_list[3]}ul.menu-list')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/projects") Projects')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/articles") Articles')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}a(href="/gospel") Gospel')
        self.lines.append(f'{self.id_list[4]}li')
        self.lines.append(f'{self.id_list[5]}button.display-switch ☀️')
    

    def __add_footer(self): 
        """
        Adds the footer section to the Pug file.
        """
        footer_content = [
            f'{self.id_list[0]}.footer',
            f'{self.id_list[1]}.footer-container',
            f'{self.id_list[2]}p Sola Scriptura ( Scripture Alone ), Solus Christus ( Christ Alone ), Sola fide ( Faith Alone ), Sola Gratia ( Grace Alone ), and Soli Deo Gloria ( Glory to God Alone )',
            f'{self.id_list[2]}.socials',
            self.__create_social_link("linkedin", "https://www.linkedin.com/in/devontaereid/", "/images/websites/linkedin.png"),
            self.__create_social_link("twitter", "https://twitter.com/_yodev_", "/images/websites/twitter.png"),
            self.__create_social_link("github", "https://github.com/y0dev", "/images/websites/github.png"),
            f'{self.id_list[2]}p.footer-small Icons provided by ',
            f'{self.id_list[3]}a(href="https://www.flaticon.com/authors/freepik" title="Freepik") Freepik'
        ]
        self.lines.extend(footer_content)

    def __create_social_link(self, platform: str, href: str, image_src: str):
        """
        Creates a social media link element for the Pug file.

        Args:
            platform: The name of the social media platform (e.g., "linkedin").
            href: The URL of the social media profile.
            image_src: The path to the social media platform icon image.

        Returns:
            A string representing the Pug code for the social media link.
        """
        return (
            f'{self.id_list[4]}li.social-links\n'
            f'{self.id_list[5]}a(href="{href}")\n'
            f'{self.id_list[6]}img(src="{image_src}")'
        )

    def __add_post_tags(self):
        """
        Adds the post tags section to the Pug file.
        """
        if not self.tags:
            return

        self.lines.append(f'{self.id_list[3]}div.post-header-tags')
        for tag in self.tags:
            self.lines.append(f'{self.id_list[5]}span.post-header-tag {tag}')

    def __add_read_time(self, indent_level: int):
        """
        Calculates and adds the estimated read time to the Pug file.

        Args:
            indent_level: The indentation level for the read time element.
        """
        time = self.post_info['time']
        timeStr = ''
        print(f'Time {time}')
        if int(time['hours']) != 0:
            if int(time['hours']) == 1:
                timeStr = '1 hour'
            else:
                timeStr = f'{int(time["hours"])} hours'
        elif int(time['mins']) != 0:
            if int(time['mins']) == 1:
                if int(time['secs']) >= 30:
                    timeStr = f'{int(time["mins"]) + 1} mins'
                else:
                    timeStr = '1 min'
            else:
                if int(time['secs']) >= 30:
                    timeStr = f'{int(time["mins"]) + 1} mins'
                else:
                    timeStr = f'{int(time["mins"])} mins'
        elif time['secs'] != '0' and time['secs'] != '00':
            timeStr = '< 1 min'

        self.lines.append(
            f'{self.id_list[indent_level]}p#post-read-time {timeStr}')
        
    
        
    def __addJavascriptFiles(self):
        self.pm.addJavascriptFile(js_filename='scripts/main.js')
        if self.code_script_added:
            self.pm.addJavascriptFile(js_filename='scripts/code_script.js')
            self.pm.addPrismCode(self.languages)
        self.pm.addBibleJavascriptFile()

    def __setupBody(self):
        self.__addNavBar()
        self.lines.append(f'{self.id_list[0]}div.post-body')
        self.lines.append(f'{self.id_list[1]}article.button#post-container')
        self.lines.append(f'{self.id_list[1]}div.post-header-container')
        self.lines.append(f'{self.id_list[2]}div.post-header-details')
        self.lines.append(f'{self.id_list[3]}h1#post-header-title {self.title}')
        self.lines.append(f'{self.id_list[3]}div.post-header-meta')
        self.lines.append(
            f'{self.id_list[4]}img.post-header-icon(src="{self.headshot}" alt="headshot")')
        self.lines.append(
            f'{self.id_list[4]}p.post-header-time {self.post_info["date"]}')
        self.lines.append(f'{self.id_list[4]}span.post-header-divider |')

        self.__addReadTime(indent_level=4)
        
        self.lines.append(
            f'{self.id_list[4]}button.post-header-shareButton#shareButton')
        self.lines.append(
            f'{self.id_list[5]}span.post-header-shareButton-icon')
        self.lines.append(
            f'{self.id_list[6]}img(src="/images/share_icon.png" alt="share_icon")')
        self.lines.append(f'{self.id_list[6]}.')
        self.lines.append(f'{self.id_list[7]}Share')

        self.__addPostTags()
        self.lines.append(
            f'{self.id_list[2]}img.post-header-image(src="/{self.post_info["image"]["name"]}" alt="{self.post_info["image"]["alt"]}")')

        self.__addPostContent()
        self.__addFooter()

        self.__addJavascriptFiles()
    
    def __addPostTags(self):
        self.lines.append(f'{self.id_list[3]}div.post-header-tags')
        for tag in self.tags:
            self.lines.append(f'{self.id_list[5]}span.post-header-tag {tag}')
    
    def __addPostContent(self):
        self.lines.append(f'{self.id_list[1]}div.post-content')
        for content in self.post_info['content']:
            new_string = ''.join(c for c in content["title"]["text"] if c.isalnum() or c == ' ')
            id_tag = f'{new_string.replace(" ","-").lower()}'
            self.lines.append(f'{self.id_list[2]}div.post-section-container#{id_tag}')
            self.lines.append(
                f'{self.id_list[3]}{content["title"]["tag"]}.section-title {content["title"]["text"]}')
            for paragraph in content['paragraphs']:
                self.__addContentParagraph(content, paragraph)
    
    def __addFooter(self):
        self.lines.append(
            f'{self.id_list[0]}.footer')
        self.lines.append(f'{self.id_list[1]}.footer-container')
        self.lines.append(f'{self.id_list[2]}p Sola Scriptura ( Scripture Alone ), Solus Christus ( Christ Alone ), Sola fide ( Faith Alone ), Sola Gratia ( Grace Alone ), and Soli Deo Gloria ( Glory to God Alone )')
        self.lines.append(f'{self.id_list[2]}.socials')
        self.lines.append(f'{self.id_list[3]}ul')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://www.linkedin.com/in/devontaereid/")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/linkedin.png")')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://twitter.com/_yodev_")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/twitter.png")')
        self.lines.append(f'{self.id_list[4]}li.social-links')
        self.lines.append(f'{self.id_list[5]}a(href="https://github.com/y0dev")')
        self.lines.append(f'{self.id_list[6]}img(src="/images/websites/github.png")')

        # Copyright
        self.lines.append(f'{self.id_list[2]}p.footer-small Icons provided by ')
        self.lines.append(f'{self.id_list[3]}a(href="https://www.flaticon.com/authors/freepik" title="Freepik") Freepik')
    
    def __addContentParagraph(self, content: dict, paragraph: str):
        pass
