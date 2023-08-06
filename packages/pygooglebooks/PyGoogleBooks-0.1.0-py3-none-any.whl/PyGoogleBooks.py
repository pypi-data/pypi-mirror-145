"""
********************************
*------------------------------*
*--------PyGoogleBooks---------*
*------------------------------*
********************************
Author: tankalxat34
Description: 
    Python package for convenient work with Google Books service
Important links:
    - GitHub: https://github.com/tankalxat34/PyGoogleBooks
    - Email: mailto:tankalxat34@gmail.com?subject=User%20of%20PyGoogleBooks
    - Telegram: https://t.me/tankalxat34
    - Telegram Channel: https://t.me/tankalxat34_official
"""

import requests, re

USER_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    "cookies": "NID=511=cF7Xznuqv-ETmVsBfjWsET4b4iUwu4jaOF1cn_uS2r9diR68Bn6M5SXMbVmYYXcSM8CqbwrX6EC87DSGkh5WjIFi2rim90P49dkoYua9QVfTbrnbySDxqo90ThIXMNHVmGSl0vxCQ5iIusdQKFG4Jy0N-_8oMK9m6qpznt8h8rA"
}

DEFAULT_LEN_ID = 12


class InvalidPageToPublicView(Exception):
    def __init__(self):
        super().__init__("This page is unavailable, or incorrect cookies are set")


class BookWithoutView(Exception):
    def __init__(self):
        super().__init__("This book does not have a preview option")


class BookWithoutAuthors(Exception):
    def __init__(self):
        super().__init__("This book doesn't have any authors")


class InvalidIdLength(Exception):
    def __init__(self):
        super().__init__("You are using ID with invalid length")


class GoogleBook:
    """Create GoogleBook object

    :param id:      The string ID of the book. It consists of 12 characters containing uppercase and lowercase Latin letters and dashes.
    :param lgp:     String parameter "lgp" in url with default value as "PA0".
    :param hl:      String parameter "hl" in url with default value as "ru".
    :param jscmd:   String parameter "jscmd" in url with default value as "click3".
    :param w:       Integer parameter with size of page. If you want to get page with good quality - use the value 1280
    """
    def __init__(self, id: str, lpg="PP1", pg="PA0", hl="ru", jscmd="click3", w=None):
        if len(id) != DEFAULT_LEN_ID:
            raise InvalidIdLength()
        self.id = id
        self.base_url = "https://books.google.ru/books"

        self.lpg = lpg
        self.pg = pg
        self.hl = hl
        self.jscmd = jscmd
        self.w = w

        self.cookies = USER_HEADERS["cookies"]
        self.dict_cookies = {"cookie": self.cookies}

        self.req = requests.get(self.base_url + f"?id={self.id}&lpg={self.lpg}&hl={self.hl}&pg={self.pg}&jscmd={self.jscmd}&w={self.w}", headers=USER_HEADERS | self.dict_cookies)
        try:
            self.json_main_response = self.req.json()
        except Exception:
            raise BookWithoutView()

        self.main_webpage_text = requests.get(self.url).text
        self.url_download = f"{self.base_url}/download/{self.name.replace(' ', '_')}.pdf?id={self.id}&output=pdf"

    @property
    def name(self):
        """Get the name of book"""
        return re.findall('<meta name="title" content="(.+?)"/>', self.main_webpage_text)[0].strip()

    @property
    def authors(self):
        """Get the list of author of book"""
        try:
            return re.findall("<title.*?>(.+?)</title>", self.main_webpage_text)[0].split("-")[1].strip().split(", ")
        except Exception:
            return ""

    @property
    def description(self):
        """Get string description of book"""
        local_result = re.findall('<meta name="description" content="(.+?)"/>', self.main_webpage_text)[0].strip()
        if '"' not in local_result:
            return local_result
        else:
            return ""

    @property
    def url(self):
        """Get url to book"""
        return self.base_url + f"?id={self.id}"

    @property
    def page_type(self):
        """Get string type of page. This type be need to get correct page-link"""
        return self.json_main_response['page'][1]['pid'][:-1]

    @property
    def cover_link(self):
        """Get link to cover of book"""
        return self.get_link_to_page(page_number=0)

    def get_link_to_page(self, page_number=1, ignore_error=False):
        """Get link to page as PNG image

        :return: String URl to png-image with page
        """
        local_req = requests.get(self.base_url + f"?id={self.id}&lpg={self.lpg}&hl={self.hl}&pg={self.page_type}{page_number}&jscmd={self.jscmd}", headers=USER_HEADERS | self.dict_cookies)
        try:
            if self.w != None:
                return local_req.json()["page"][0]["src"]+f"&w={self.w}"
            else:
                return local_req.json()["page"][0]["src"]
        except Exception:
            if not ignore_error:
                raise InvalidPageToPublicView()


    def get_pages(self, last_page_number: int, ignore_errors=False):
        """Get links to pages

        :return: List with URls to png-images with pages
        """
        local_list = []
        for page_number in range(last_page_number):
            try:
                local_list.append(self.get_link_to_page(page_number, ignore_errors))
            except Exception:
                if ignore_errors:
                    local_list.append(None)
        return local_list
