import json
import requests
from bs4 import BeautifulSoup
from src.googlesearch import GoogleEngine
from src.handler import ErrorHanlder
import re
from src.utils import get_content_until
import hashlib


class GenericWeb:
    def __init__(self, base_url: str, web_name: str):
        self._base_url: str = base_url
        self._web_name: str = web_name
        self._session: requests.Session = requests.Session()
        self._raw_content: str = None
        self._json_content: str = None

    def _get_raw_content(self) -> bytes:
        res = self._session.get(self._base_url)
        res.raise_for_status()
        return res.content

    def _parse_json(self) -> json:
        jsonObject = json.loads(self._raw_content)
        self._json_content = jsonObject
        return self._json_content

    # TODO: 解決 Json 與 非Json 內容問題

    def init(self):
        self._raw_content = self._get_raw_content(self)


class TaiwanFactCheck(GenericWeb):
    def __init__(self):
        # TODO: 解決 google search api 的問題

        base_url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=20&hl=zh-TW&source=gcsc&gss=.tw&cselibv=8435450f13508ca1&cx=016739345681392223711%3Aurihlbomoaq&q=%E8%A9%90%E9%A8%99%2B%E5%BE%B5&safe=off&cse_tok=AB-tC_7rAJHN0PV3JSKDiJwvzPd1%3A1706406801809&sort=&exp=cc%2Cdtsq-3&fexp=72485384%2C72485385&callback=google.search.cse.api8754"
        web_name = "TaiwanFactCheck"
        super().__init__(base_url, web_name)

        self.sub_links = []
        self.result = []

    def get_sub_links(self):
        results = GoogleEngine().search("詐騙+徵才").get_all_links()

        for link in results:
            if "https://tfc-taiwan.org.tw/articles/" not in link:
                continue
            self.sub_links.append(link)
        return self.sub_links

    def get_page_content(self, link):
        res = self._session.get(link)

        if res.status_code > 400:
            return None

        soup = BeautifulSoup(res.content.decode("utf-8"), "html.parser")
        titles = soup.find_all("h2")
        head_tag_find = list(filter(lambda h2: h2.text == "背景", titles))
        head_tag = head_tag_find[0] if len(head_tag_find) > 0 else None
        if head_tag is None:
            return None
        content = get_content_until("h2", head_tag, include_head=False)
        return content

    def get_result(self):
        for link in self.sub_links:
            content = self.get_page_content(link)
            if content is None:
                continue
            self.result.append(content)
        return self.result

    def save(self, path):
        to_save = [[hashlib.md5(x.encode("utf-8")).hexdigest(), x] for x in self.result]
        with open(path, "w", encoding="utf-8") as wf:
            json.dump(to_save, wf, ensure_ascii=False, indent=4)
