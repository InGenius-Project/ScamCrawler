import json
import requests
from Src.handler import ErrorHanlder
import re

class GenericWeb:
    def __init__(self, base_url: str, web_name: str):
        self._base_url: str = base_url
        self._web_name: str = web_name
        self._session: requests.Session = requests.Session()
        self._raw_content: str = None
        self._json_content: str = None
    
    @ErrorHanlder.request_error
    def _get_raw_content(self) -> bytes:
        res = self._session.get(self._base_url)
        res.raise_for_status()
        return res.content

    def _parse_json(self, raw_content) -> json:
        jsonObject = json.loads(self._raw_content)
        self._json_content = jsonObject
        return self._json_content
    
    # TODO: 解決 Json 與 非Json 內容問題

    def init(self):
        self._raw_content = self._get_raw_content(self)
    
    
class TaiwanFactCheck(GenericWeb):
    def __init__(self):
        base_url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=zh-TW&source=gcsc&gss=.tw&cselibv=3bd4ac03c21554b3&cx=016739345681392223711%3Aurihlbomoaq&q=%E5%BE%B5%E6%89%8D+%E9%8C%AF%E8%AA%A4+%E8%A9%90%E9%A8%99&safe=off&cse_tok=AB-tC_46pyznbk9agghdlTs-qKAB%3A1703828960242&sort=&exp=csqr%2Ccc%2Cdtsq-3&callback=google.search.cse.api1505"
        web_name = "TaiwanFactCheck"
        super().__init__(base_url, web_name)
    
    def get_raw_content(self) -> str:
        self._raw_content = super().get_raw_content()
        raw_content = self._raw_content.decode("utf-8").replace("\n", "")
        result = re.search(r"google.search.cse.api\d+\((.*)\)", raw_content)
        if result: 
            self._raw_content = result.group(1)
            return self._raw_content
        raise Exception("Regex Error.")

    def _parse_json(self) -> json:
        self._json_content = super()._parse_json()
        return self._json_content
    