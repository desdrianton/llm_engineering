import requests
from bs4 import BeautifulSoup

class WebRetriever:
    __HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    __url : str = None
    __title : str = None
    __body : str = None
    __soup : BeautifulSoup = None
    __res = None
    __links = {}

    def __init__(self, *, url : str):
        self.__url = url

    def __request(self):
        self.__res = requests.get(self.__url, headers=self.__HEADERS)

    def __parsing(self):
        self.__soup = BeautifulSoup(self.__res.content, "html.parser")
        self.__title = self.__soup.title.string if self.__soup.title else "No title found"
        for irrelevant in self.__soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.__body = self.__soup.body.get_text(separator="\n", strip=True)

    def retrieve(self):
        self.__request()
        self.__parsing()

        return self.__title, self.__body

    def generate_links(self):
        self.__links = {link.get("href") for link in self.__soup.find_all("a")}
        return self.__links

    def get_url(self) -> str:
        return self.__url

    def get_soup(self) -> BeautifulSoup:
        return self.__soup

    def get_links(self):
        return self.__links

    def get_contents(self):
        return f"Webpage Title:\n{self.__title}\nWebpage Contents:\n{self.__body}\n\n"
