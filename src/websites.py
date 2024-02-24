from abc import abstractmethod
from sys import stdout
import json
import requests
from typing import List
from bs4 import BeautifulSoup, SoupStrainer, Tag
from src.googlesearch import GoogleEngine
from src.utils import get_content_until
import hashlib
from src.analyzer import PageAnalyzer104
from time import sleep


class GenericWeb:
    def __init__(self, base_url: str, web_name: str, save_path: str):
        self._base_url: str = base_url
        self._web_name: str = web_name
        self._session: requests.Session = requests.Session()
        self._raw_content: bytes | None = None
        self._result: List[str] = []
        self._save_path: str = save_path
        self._progress: float = 0.0

    def _get_raw_content(self) -> bytes:
        res = self._session.get(self._base_url)
        res.raise_for_status()
        return res.content

    @abstractmethod
    def get_result(self) -> List[str]:
        pass

    def get_save_path(self) -> str:
        return self._save_path

    def get_progress(self) -> float:
        return self._progress

    def print_progress(self) -> None:
        percent = self._progress
        format_percent = "{:5}".format(percent)
        stdout.write(f"\r{self._web_name}: {format_percent}% [DATA: {len(self._result)}]")
        stdout.flush()

    def save(self, path: str | None = None, label: int = 3) -> None:
        self._save_path = self._save_path if path is None else path
        self._result = list(set(self._result))
        to_save = [
            {
                "id": hashlib.md5(x.encode("utf-8")).hexdigest(),
                "content": x,
                "label": label,
            }
            for x in self._result
        ]
        with open(self._save_path, "w", encoding="utf-8") as wf:
            json.dump(to_save, wf, ensure_ascii=False, indent=4)

    def start_and_save(self, path: str | None = None, label: int = 3) -> None:
        self.get_result()
        self.save(path, label)


class HumanBank104(GenericWeb):
    def __init__(self):
        base_url = "https://www.104.com.tw/jobs/search/?keyword=%E5%AF%A6%E7%BF%92"
        web_name = "104 人力銀行"
        save_path = "results/humanbank104.json"
        super().__init__(base_url, web_name, save_path)

        # Use selenium
        from src.utils import SeleniumDriver
        self._selenium_driver = SeleniumDriver()

        self._origin_url = self._base_url
        self._min_page = 0
        self._max_page = 100
        self._current_page = 1
        self._sleep_time = 1
        self.debug = True

    def _get_raw_content(self) -> bytes:
        return super()._get_raw_content()

    def _get_page_content(self, page_source: str) -> str | None:
        pga104 = PageAnalyzer104(page_source)
        job = pga104.get_job()
        if job is None:
            return None
        return job.combine()

    def _get_sub_links(self) -> List[str]:
        raw_content = self._get_raw_content()
        soup = BeautifulSoup(raw_content, "html.parser", parse_only=SoupStrainer("a"))
        results = list(filter(lambda y: "//www.104.com.tw/job/" in y ,[ "https:" + x["href"] for x in soup]))
        return results

    def get_result(self) -> List[str]:
        while self._current_page < self._max_page:
            self._base_url = self._origin_url + f"&page={self._current_page}"
            links = self._get_sub_links() 
            for link in links:
                self._selenium_driver.get(link)
                page_source = self._selenium_driver.get_content()
                if page_source is None:
                    continue
                content = self._get_page_content(page_source)
                if content is None:
                    continue
                self._result.append(content)
                self._progress = round((self._current_page / self._max_page) * 100, 2)
                self.print_progress()
            self._current_page += 1
            if self.debug:
                break
            sleep(self._sleep_time)
        print()
        self._selenium_driver.quit()
        return self._result


class TaiwanFactCheck(GenericWeb):
    def __init__(self):
        base_url = ""
        web_name = "TaiwanFactCheck"
        save_path = "results/taiwanfackcheck.json"
        super().__init__(base_url, web_name, save_path)

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

    def get_result(self) -> List[str]:
        for link in self.sub_links:
            content = self.get_page_content(link)
            if content is None:
                continue
            content = content.replace("\n", "")
            self.result.append(content)
        return self.result
