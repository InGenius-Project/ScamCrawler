import json
import requests
from bs4 import BeautifulSoup
from src.handler import ErrorHanlder
import re
from src.utils import get_content_until

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
    
    def get_raw_content(self) -> str:
        self._raw_content = super()._get_raw_content()
        raw_content = self._raw_content.decode("utf-8").replace("\n", "")
        result = re.search(r"google.search.cse.api\d+\((.*)\)", raw_content)
        if result: 
            self._raw_content = result.group(1)
            return self._raw_content
        raise Exception("Regex Error.")

    def get_parsed_json(self) -> json:
        self._json_content = super()._parse_json()
        return self._json_content

    def get_sub_links(self):
        result = self._json_content["results"]

        for i in range(len(result)):
            try:
                link = result[i]["url"]
                title = result[i]["richSnippet"]["metatags"]["ogTitle"]
                
                if not (("詐騙" in title or "錯誤" in title) and "徵" in title):
                    continue
                if "https://tfc-taiwan.org.tw/articles/" not in link:
                    continue
                self.sub_links.append(link)
            except:
                pass
        return self.sub_links

    def get_page_content(self, link):
        re = self._session.get(link)
        
        if re.status_code > 400:
            return None
        
        soup = BeautifulSoup(re.content.decode("utf-8"), "html.parser")
        titles = soup.find_all("h2")
        head_tag = list(filter(lambda h2: h2.text == "背景", titles))[0]
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
        with open(path, "w", encoding="utf-8") as wf:
            json.dump(self.result, wf, ensure_ascii=False, indent=4)