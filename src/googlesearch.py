from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_KEY = os.getenv("GOOGLE_CSE_KEY")


class GoogleEngine:
    class SearchResult:
        def __init__(self, result):
            self.raw_content = result

        def get_all_result(self):
            return [
                {"title": x.get("title"), "link": x.get("link")}
                for x in self.raw_content
            ]

        def get_all_links(self):
            return [x.get("link") for x in self.raw_content]

        def get_all_titles(self):
            return [x.get("title") for x in self.raw_content]

    def __init__(self):
        self.API_KEY = API_KEY
        self.CSE_KEY = CSE_KEY
        self.service = build("customsearch", "v1", developerKey=self.API_KEY).cse()
        self.result = None

    def search(self, search_term):
        result = self.service.list(q=search_term, cx=self.CSE_KEY).execute()["items"]
        return self.SearchResult(result)
